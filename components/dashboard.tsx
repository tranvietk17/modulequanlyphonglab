"use client"

import { useState, useEffect } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Textarea } from "@/components/ui/textarea"
import { Calendar, Clock, CheckCircle, XCircle, Users, Edit, BookOpen } from "lucide-react"
import { useAppContext } from "./app-context"

interface DashboardProps {
  userRole: "student" | "admin"
  language: "vi" | "en"
  currentUserEmail: string
}

export function Dashboard({ userRole, language, currentUserEmail }: DashboardProps) {
  const { bookings, equipment, users, addBooking, updateBooking, updateUser, updateEquipment, getUserByEmail } =
    useAppContext()

  const [newBooking, setNewBooking] = useState({
    equipment: "",
    department: "",
    room: "",
    date: "",
    pickupTime: "",
    returnTime: "",
    purpose: "",
  })

  const [selectedBooking, setSelectedBooking] = useState<any>(null)
  const [showBookingDetails, setShowBookingDetails] = useState(false)

  const [editingEquipment, setEditingEquipment] = useState<any>(null)
  const [showEquipmentEdit, setShowEquipmentEdit] = useState(false)

  const [editingUser, setEditingUser] = useState<any>(null)
  const [showUserEdit, setShowUserEdit] = useState(false)

  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content:
        language === "vi"
          ? "Xin chào! Tôi là AI Assistant. Tôi có thể giúp bạn đặt lịch thiết bị, tìm kiếm thông tin và trả lời câu hỏi."
          : "Hello! I'm your AI Assistant. I can help you book equipment, find information, and answer questions.",
    },
  ])
  const [chatInput, setChatInput] = useState("")

  const [departments] = useState([
    { id: 1, name: "Khoa Sinh học", rooms: ["Lab B101", "Lab B102", "Lab B103"] },
    { id: 2, name: "Khoa Vật lý", rooms: ["Lab P205", "Lab P206", "Lab P207"] },
    { id: 3, name: "Khoa Hóa học", rooms: ["Lab C301", "Lab C302", "Lab C303"] },
    { id: 4, name: "Khoa Công nghệ thông tin", rooms: ["Lab IT401", "Lab IT402", "Lab IT403"] },
  ])

  const currentUser = getUserByEmail(currentUserEmail)

  const filteredBookings = bookings.filter((booking) => {
    if (userRole === "student") {
      return booking.studentEmail === currentUserEmail
    }
    return true // Admin thấy tất cả bookings
  })

  useEffect(() => {
    const interval = setInterval(() => {
      console.log("[v0] Real-time update check")
    }, 30000)
    return () => clearInterval(interval)
  }, [])

  const [activeBookings, setActiveBookings] = useState([])
  const [setLanguage, setEquipment, setUsers] = [() => {}, () => {}, () => {}]

  const handleNewBooking = () => {
    if (!newBooking.equipment || !newBooking.date || !newBooking.pickupTime || !newBooking.returnTime) {
      alert(language === "vi" ? "Vui lòng điền đầy đủ thông tin!" : "Please fill in all fields!")
      return
    }

    const selectedEquipment = equipment.find((eq) => eq.name === newBooking.equipment)
    if (!selectedEquipment) {
      alert(language === "vi" ? "Thiết bị không tồn tại!" : "Equipment not found!")
      return
    }

    if (selectedEquipment.available <= 0) {
      alert(language === "vi" ? "Thiết bị này hiện không có sẵn!" : "This equipment is currently not available!")
      return
    }

    // Giảm số lượng thiết bị có sẵn
    updateEquipment(selectedEquipment.id, {
      available: selectedEquipment.available - 1,
      status: selectedEquipment.available - 1 <= 0 ? "in-use" : "available",
    })

    addBooking({
      equipment: newBooking.equipment,
      department: selectedEquipment.department,
      room: selectedEquipment.room,
      date: newBooking.date,
      pickupTime: newBooking.pickupTime,
      returnTime: newBooking.returnTime,
      status: "pending",
      studentName: currentUser?.name || "Unknown",
      studentEmail: currentUserEmail,
      purpose: newBooking.purpose,
    })

    setNewBooking({
      equipment: "",
      department: "",
      room: "",
      date: "",
      pickupTime: "",
      returnTime: "",
      purpose: "",
    })

    alert(language === "vi" ? "Đặt lịch thành công!" : "Booking successful!")
  }

  const handleApproval = async (bookingId: number, action: "approve" | "reject") => {
    updateBooking(bookingId, { status: action === "approve" ? "approved" : "rejected" })

    // Simulate email sending with AI-generated content
    const booking = bookings.find((b) => b.id === bookingId)
    if (booking) {
      await sendAIGeneratedEmail(booking, action)
    }

    alert(
      language === "vi"
        ? `${action === "approve" ? "Phê duyệt" : "Từ chối"} thành công! Email thông báo đã được gửi.`
        : `${action === "approve" ? "Approved" : "Rejected"} successfully! Notification email sent.`,
    )
  }

  const rejectBooking = (bookingId: number) => {
    updateBooking(bookingId, { status: "rejected" })
    alert(language === "vi" ? "Đã từ chối đơn đặt lịch!" : "Booking rejected!")
  }

  const editEquipment = (eq: any) => {
    setEditingEquipment({ ...eq })
    setShowEquipmentEdit(true)
  }

  const saveEquipmentChanges = () => {
    updateEquipment(editingEquipment.id, editingEquipment)
    setShowEquipmentEdit(false)
    setEditingEquipment(null)
    alert(language === "vi" ? "Cập nhật thiết bị thành công!" : "Equipment updated successfully!")
  }

  const editUser = (user: any) => {
    setEditingUser({ ...user })
    setShowUserEdit(true)
  }

  const saveUserChanges = () => {
    updateUser(editingUser.id, editingUser)
    setShowUserEdit(false)
    setEditingUser(null)
    alert(language === "vi" ? "Cập nhật người dùng thành công!" : "User updated successfully!")
  }

  const toggleUserStatus = (userId: number) => {
    const user = users.find((u) => u.id === userId)
    if (user) {
      updateUser(userId, {
        status: user.status === "active" ? "inactive" : "active",
      })
    }
  }

  const t = {
    vi: {
      dashboard: "Bảng điều khiển",
      myBookings: "Lịch đặt của tôi",
      newBooking: "Đặt lịch mới",
      equipment: "Thiết bị",
      users: "Người dùng",
      reports: "Báo cáo",
      settings: "Cài đặt",
      rooms: "Phòng lab",
      approval: "Xét duyệt",
      totalBookings: "Tổng lượt đặt",
      activeBookings: "Đang hoạt động",
      pendingApproval: "Chờ duyệt",
      completedBookings: "Đã hoàn thành",
      approved: "Đã duyệt",
      pending: "Chờ duyệt",
      rejected: "Từ chối",
      department: "Khoa",
      room: "Phòng",
      date: "Ngày",
      time: "Thời gian",
      status: "Trạng thái",
      pickupTime: "Giờ nhận",
      returnTime: "Giờ trả",
      purpose: "Mục đích sử dụng",
      selectEquipment: "Chọn thiết bị",
      selectDepartment: "Chọn khoa",
      selectRoom: "Chọn phòng",
      bookNow: "Đặt lịch ngay",
      approve: "Phê duyệt",
      reject: "Từ chối",
      sendEmail: "Gửi email",
      aiAssistant: "Trợ lý AI",
      askAI: "Hỏi AI...",
      send: "Gửi",
      details: "Chi tiết",
      edit: "Chỉnh sửa",
      save: "Lưu",
      cancel: "Hủy",
      bookingDetails: "Chi tiết đặt lịch",
      editEquipment: "Chỉnh sửa thiết bị",
      equipmentName: "Tên thiết bị",
      description: "Mô tả",
      specifications: "Thông số kỹ thuật",
      available: "Có sẵn",
      inUse: "Đang sử dụng",
      aiChat: "Trợ lý AI",
    },
    en: {
      dashboard: "Dashboard",
      myBookings: "My Bookings",
      newBooking: "New Booking",
      equipment: "Equipment",
      users: "Users",
      reports: "Reports",
      settings: "Settings",
      rooms: "Lab Rooms",
      approval: "Approval",
      totalBookings: "Total Bookings",
      activeBookings: "Active",
      pendingApproval: "Pending",
      completedBookings: "Completed",
      approved: "Approved",
      pending: "Pending",
      rejected: "Rejected",
      department: "Department",
      room: "Room",
      date: "Date",
      time: "Time",
      status: "Status",
      pickupTime: "Pickup Time",
      returnTime: "Return Time",
      purpose: "Purpose",
      selectEquipment: "Select Equipment",
      selectDepartment: "Select Department",
      selectRoom: "Select Room",
      bookNow: "Book Now",
      approve: "Approve",
      reject: "Reject",
      sendEmail: "Send Email",
      aiAssistant: "AI Assistant",
      askAI: "Ask AI...",
      send: "Send",
      details: "Details",
      edit: "Edit",
      save: "Save",
      cancel: "Cancel",
      bookingDetails: "Booking Details",
      editEquipment: "Edit Equipment",
      equipmentName: "Equipment Name",
      description: "Description",
      specifications: "Specifications",
      available: "Available",
      inUse: "In Use",
      aiChat: "AI Chat",
    },
  }

  const currentLang = t[language]

  const showBookingDetailsModal = (booking: any) => {
    setSelectedBooking(booking)
    setShowBookingDetails(true)
  }

  const handleBookingSubmit = async () => {
    if (!newBooking.equipment || !newBooking.date || !newBooking.pickupTime || !newBooking.returnTime) {
      alert(language === "vi" ? "Vui lòng điền đầy đủ thông tin!" : "Please fill in all required fields!")
      return
    }

    const selectedEquipment = equipment.find((eq) => eq.name === newBooking.equipment)
    if (!selectedEquipment) {
      alert(language === "vi" ? "Thiết bị không tồn tại!" : "Equipment not found!")
      return
    }

    if (selectedEquipment.available <= 0) {
      alert(language === "vi" ? "Thiết bị này hiện không có sẵn!" : "This equipment is currently not available!")
      return
    }

    // Simulate AI risk assessment
    const aiRiskAssessment = await simulateAIRiskAssessment(newBooking)

    // Giảm số lượng thiết bị có sẵn
    updateEquipment(selectedEquipment.id, {
      available: selectedEquipment.available - 1,
      status: selectedEquipment.available - 1 <= 0 ? "in-use" : "available",
    })

    // Sử dụng addBooking từ context thay vì state local
    addBooking({
      equipment: newBooking.equipment,
      department: selectedEquipment.department,
      room: selectedEquipment.room,
      date: newBooking.date,
      pickupTime: newBooking.pickupTime,
      returnTime: newBooking.returnTime,
      status: "pending",
      studentName: currentUser?.name || "Unknown",
      studentEmail: currentUserEmail,
      purpose: newBooking.purpose,
    })

    setNewBooking({
      equipment: "",
      department: "",
      room: "",
      date: "",
      pickupTime: "",
      returnTime: "",
      purpose: "",
    })

    alert(
      language === "vi"
        ? "Đặt lịch thành công! AI đã đánh giá rủi ro: " + aiRiskAssessment
        : "Booking successful! AI risk assessment: " + aiRiskAssessment,
    )
  }

  const simulateAIRiskAssessment = async (booking: any) => {
    // Simulate GPT-3.5 API call for risk assessment
    const risks = []

    if (booking.pickupTime === booking.returnTime) {
      risks.push(language === "vi" ? "Thời gian sử dụng quá ngắn" : "Usage time too short")
    }

    const pickupHour = Number.parseInt(booking.pickupTime.split(":")[0])
    if (pickupHour < 8 || pickupHour > 17) {
      risks.push(language === "vi" ? "Ngoài giờ hành chính" : "Outside office hours")
    }

    return {
      level: risks.length > 0 ? "medium" : "low",
      issues: risks,
      recommendation:
        risks.length > 0
          ? language === "vi"
            ? "Cần xem xét kỹ"
            : "Requires careful review"
          : language === "vi"
            ? "An toàn để phê duyệt"
            : "Safe to approve",
    }
  }

  const sendAIGeneratedEmail = async (booking: any, action: "approve" | "reject") => {
    // Simulate GPT-3.5 email generation
    const emailContent =
      action === "approve"
        ? language === "vi"
          ? `Kính gửi ${booking.studentName},\n\nĐơn đặt lịch thiết bị "${booking.equipment}" của bạn đã được phê duyệt.\n\nThời gian: ${booking.date} từ ${booking.pickupTime} đến ${booking.returnTime}\nPhòng: ${booking.room}\n\nVui lòng đến đúng giờ và tuân thủ quy định sử dụng thiết bị.\n\nTrân trọng,\nBộ phận Quản lý Lab DNU`
          : `Dear ${booking.studentName},\n\nYour equipment booking for "${booking.equipment}" has been approved.\n\nTime: ${booking.date} from ${booking.pickupTime} to ${booking.returnTime}\nRoom: ${booking.room}\n\nPlease arrive on time and follow equipment usage guidelines.\n\nBest regards,\nDNU Lab Management`
        : language === "vi"
          ? `Kính gửi ${booking.studentName},\n\nRất tiếc, đơn đặt lịch thiết bị "${booking.equipment}" của bạn đã bị từ chối.\n\nLý do: Cần bổ sung thêm thông tin hoặc xung đột lịch trình.\n\nVui lòng liên hệ để được hỗ trợ.\n\nTrân trọng,\nBộ phận Quản lý Lab DNU`
          : `Dear ${booking.studentName},\n\nWe regret to inform you that your equipment booking for "${booking.equipment}" has been rejected.\n\nReason: Additional information needed or schedule conflict.\n\nPlease contact us for assistance.\n\nBest regards,\nDNU Lab Management`

    console.log("[v0] AI-generated email sent:", emailContent)
  }

  const handleChatSubmit = async () => {
    if (!chatInput.trim()) return

    const userMessage = { role: "user", content: chatInput }
    setChatMessages((prev) => [...prev, userMessage])

    // Simulate GPT-3.5 response
    const aiResponse = await simulateGPTResponse(chatInput, language)
    setChatMessages((prev) => [...prev, { role: "assistant", content: aiResponse }])
    setChatInput("")
  }

  const simulateGPTResponse = async (input: string, lang: string) => {
    await new Promise((resolve) => setTimeout(resolve, 1500))

    const lowerInput = input.toLowerCase()

    // AI Web Control Commands
    if (lowerInput.includes("tạo booking") || lowerInput.includes("create booking")) {
      // AI can create bookings
      const newBooking = {
        id: Date.now(),
        studentName: currentUser.name,
        equipment: "Máy ly tâm",
        date: new Date().toISOString().split("T")[0],
        pickupTime: "09:00",
        returnTime: "11:00",
        room: "Lab B101",
        status: "pending",
        purpose: "AI tự động tạo booking",
      }
      setActiveBookings((prev) => [...prev, newBooking])
      return lang === "vi"
        ? "✅ Tôi đã tạo booking mới cho bạn! Máy ly tâm - Lab B101, 9:00-11:00 hôm nay. Kiểm tra tab 'Lịch đặt của tôi'."
        : "✅ I've created a new booking for you! Centrifuge - Lab B101, 9:00-11:00 today. Check 'My Bookings' tab."
    }

    if (lowerInput.includes("phê duyệt tất cả") || lowerInput.includes("approve all")) {
      // AI can approve all pending bookings
      setActiveBookings((prev) =>
        prev.map((booking) => (booking.status === "pending" ? { ...booking, status: "approved" } : booking)),
      )
      return lang === "vi"
        ? "✅ Tôi đã phê duyệt tất cả đơn đặt lịch đang chờ! Email thông báo sẽ được gửi tự động."
        : "✅ I've approved all pending bookings! Notification emails will be sent automatically."
    }

    if (lowerInput.includes("thay đổi ngôn ngữ") || lowerInput.includes("change language")) {
      setLanguage((prev) => (prev === "vi" ? "en" : "vi"))
      return lang === "vi"
        ? "✅ Đã chuyển sang tiếng Anh! Language changed to English."
        : "✅ Đã chuyển sang tiếng Việt! Language changed to Vietnamese."
    }

    if (lowerInput.includes("tạo thiết bị") || lowerInput.includes("create equipment")) {
      const newEquipment = {
        id: Date.now(),
        name: "Thiết bị AI tạo",
        department: "Khoa Sinh học",
        room: "Lab B101",
        available: true,
        description: "Thiết bị được tạo bởi AI Assistant",
        specifications: "Tự động tạo bởi AI",
      }
      setEquipment((prev) => [...prev, newEquipment])
      return lang === "vi"
        ? "✅ Tôi đã tạo thiết bị mới! Kiểm tra tab 'Thiết bị' để xem chi tiết."
        : "✅ I've created new equipment! Check 'Equipment' tab for details."
    }

    if (lowerInput.includes("tạo user") || lowerInput.includes("create user")) {
      const newUser = {
        id: Date.now(),
        name: "User AI tạo",
        email: `ai-user-${Date.now()}@dnu.edu.vn`,
        role: "student",
        department: "Khoa Sinh học",
        status: "active",
      }
      setUsers((prev) => [...prev, newUser])
      return lang === "vi"
        ? "✅ Tôi đã tạo user mới! Kiểm tra tab 'Người dùng' để xem danh sách."
        : "✅ I've created a new user! Check 'Users' tab to see the list."
    }

    if (lowerInput.includes("thống kê") || lowerInput.includes("statistics")) {
      const totalBookings = bookings.length
      const approvedBookings = bookings.filter((b) => b.status === "approved").length
      const availableEquipment = equipment.filter((e) => e.available).length
      const activeUsers = users.filter((u) => u.status === "active").length

      return lang === "vi"
        ? `📊 THỐNG KÊ HỆ THỐNG:\n\n• Tổng booking: ${totalBookings}\n• Đã phê duyệt: ${approvedBookings}\n• Thiết bị có sẵn: ${availableEquipment}/${equipment.length}\n• User hoạt động: ${activeUsers}/${users.length}\n• Phòng lab: ${departments.reduce((acc, dept) => acc + dept.rooms.length, 0)}`
        : `📊 SYSTEM STATISTICS:\n\n• Total bookings: ${totalBookings}\n• Approved: ${approvedBookings}\n• Available equipment: ${availableEquipment}/${equipment.length}\n• Active users: ${activeUsers}/${users.length}\n• Lab rooms: ${departments.reduce((acc, dept) => acc + dept.rooms.length, 0)}`
    }

    // Advanced general knowledge responses
    if (lowerInput.includes("thời tiết") || lowerInput.includes("weather")) {
      return lang === "vi"
        ? "🌤️ Tôi không thể kiểm tra thời tiết trực tiếp, nhưng có thể gợi ý:\n\n• Hôm nay ở Đà Nẵng thường 25-30°C\n• Mùa mưa: tháng 9-12\n• Mùa khô: tháng 1-8\n• Apps tốt: AccuWeather, Weather.com\n\nNgoài ra tôi có thể điều khiển toàn bộ hệ thống lab này!"
        : "🌤️ I can't check weather directly, but here are tips:\n\n• Da Nang usually 25-30°C today\n• Rainy season: Sep-Dec\n• Dry season: Jan-Aug\n• Good apps: AccuWeather, Weather.com\n\nBesides, I can control this entire lab system!"
    }

    if (lowerInput.includes("tin tức") || lowerInput.includes("news")) {
      return lang === "vi"
        ? "📰 Tin tức hôm nay:\n\n• Công nghệ: AI đang phát triển mạnh\n• Giáo dục: Đại học số hóa tăng\n• Khoa học: Nghiên cứu y sinh học tiến bộ\n• Nguồn tin: VnExpress, Tuổi Trẻ, BBC\n\nTôi cũng có thể quản lý toàn bộ hệ thống lab - thử hỏi 'tạo booking' hoặc 'phê duyệt tất cả'!"
        : "📰 Today's news:\n\n• Tech: AI developing rapidly\n• Education: University digitization rising\n• Science: Biomedical research advancing\n• Sources: BBC, CNN, Reuters\n\nI can also manage the entire lab system - try asking 'create booking' or 'approve all'!"
    }

    if (lowerInput.includes("nấu ăn") || lowerInput.includes("cooking") || lowerInput.includes("recipe")) {
      return lang === "vi"
        ? "👨‍🍳 Công thức nấu ăn phổ biến:\n\n• Phở: Xương bò + gia vị + bánh phở\n• Cơm tấm: Thịt nướng + trứng + nước mắm\n• Bánh mì: Bánh + pate + thịt + rau\n• Apps: Cookpad, YouTube\n\nNhưng tôi giỏi hơn ở việc quản lý lab! Thử hỏi 'tạo thiết bị' hoặc 'thống kê hệ thống'!"
        : "👨‍🍳 Popular recipes:\n\n• Pho: Beef bones + spices + noodles\n• Pasta: Noodles + sauce + cheese\n• Sandwich: Bread + meat + vegetables\n• Apps: Cookpad, YouTube\n\nBut I'm better at lab management! Try asking 'create equipment' or 'system statistics'!"
    }

    if (lowerInput.includes("toán học") || lowerInput.includes("math") || lowerInput.includes("tính toán")) {
      return lang === "vi"
        ? "🧮 Tôi có thể giải toán cơ bản:\n\n• Cộng trừ nhân chia\n• Phương trình bậc 2\n• Tính diện tích, thể tích\n• Thống kê cơ bản\n\nVí dụ: 2+2=4, √16=4, π≈3.14\n\nNhưng sở trường của tôi là điều khiển hệ thống lab! Thử 'tạo user' hoặc 'thay đổi ngôn ngữ'!"
        : "🧮 I can solve basic math:\n\n• Addition, subtraction, multiplication, division\n• Quadratic equations\n• Area, volume calculations\n• Basic statistics\n\nExample: 2+2=4, √16=4, π≈3.14\n\nBut my specialty is controlling the lab system! Try 'create user' or 'change language'!"
    }

    // Equipment booking assistance
    if (
      lowerInput.includes("mượn") ||
      lowerInput.includes("đặt lịch") ||
      lowerInput.includes("book") ||
      lowerInput.includes("borrow")
    ) {
      const availableEquipment = equipment.filter((eq) => eq.available > 0)
      return lang === "vi"
        ? `🔬 Tôi có thể giúp bạn đặt lịch! Hiện có ${availableEquipment.length} thiết bị:\n\n${availableEquipment
            .slice(0, 3)
            .map((eq) => `• ${eq.name} (${eq.department})`)
            .join("\n")}\n\n💡 Thử nói: "tạo booking" để tôi tự động tạo đơn cho bạn!`
        : `🔬 I can help you book equipment! Currently ${availableEquipment.length} available:\n\n${availableEquipment
            .slice(0, 3)
            .map((eq) => `• ${eq.name} (${eq.department})`)
            .join("\n")}\n\n💡 Try saying: "create booking" for me to automatically create one!`
    }

    // Default powerful AI response
    return lang === "vi"
      ? `🤖 Tôi là AI Assistant siêu mạnh của DNU Lab! Tôi có thể:\n\n🎯 ĐIỀU KHIỂN HỆ THỐNG:\n• "tạo booking" - Tự động đặt lịch\n• "phê duyệt tất cả" - Duyệt tất cả đơn\n• "tạo thiết bị" - Thêm thiết bị mới\n• "tạo user" - Tạo người dùng\n• "thay đổi ngôn ngữ" - Chuyển VI/EN\n• "thống kê" - Xem báo cáo\n\n🌍 TRẢ LỜI MỌI THỨ:\n• Thời tiết, tin tức, nấu ăn\n• Toán học, khoa học\n• Lời khuyên cuộc sống\n\nHãy thử một lệnh nào đó!`
      : `🤖 I'm DNU Lab's super powerful AI Assistant! I can:\n\n🎯 CONTROL SYSTEM:\n• "create booking" - Auto book equipment\n• "approve all" - Approve all requests\n• "create equipment" - Add new equipment\n• "create user" - Create new user\n• "change language" - Switch VI/EN\n• "statistics" - View reports\n\n🌍 ANSWER EVERYTHING:\n• Weather, news, cooking\n• Math, science\n• Life advice\n\nTry a command!`
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case "approved":
        return (
          <Badge className="bg-green-600">
            <CheckCircle className="w-3 h-3 mr-1" />
            {currentLang.approved}
          </Badge>
        )
      case "pending":
        return (
          <Badge variant="secondary">
            <Clock className="w-3 h-3 mr-1" />
            {currentLang.pending}
          </Badge>
        )
      case "rejected":
        return (
          <Badge variant="destructive">
            <XCircle className="w-3 h-3 mr-1" />
            {currentLang.rejected}
          </Badge>
        )
      default:
        return <Badge variant="outline">{status}</Badge>
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <h1 className="text-2xl font-bold text-gray-900">{currentLang.dashboard}</h1>
            <div className="flex items-center space-x-4">
              <Badge variant="outline" className="capitalize">
                {userRole === "student"
                  ? language === "vi"
                    ? "Sinh viên"
                    : "Student"
                  : language === "vi"
                    ? "Quản trị"
                    : "Admin"}
              </Badge>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{currentLang.totalBookings}</CardTitle>
              <Calendar className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{bookings.length}</div>
              <p className="text-xs text-muted-foreground">
                +12% {language === "vi" ? "từ tháng trước" : "from last month"}
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{currentLang.activeBookings}</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{bookings.filter((b) => b.status === "approved").length}</div>
              <p className="text-xs text-muted-foreground">{language === "vi" ? "Đang sử dụng" : "Currently active"}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{currentLang.pendingApproval}</CardTitle>
              <Clock className="h-4 w-4 text-yellow-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{bookings.filter((b) => b.status === "pending").length}</div>
              <p className="text-xs text-muted-foreground">{language === "vi" ? "Cần xem xét" : "Awaiting review"}</p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">{currentLang.completedBookings}</CardTitle>
              <Users className="h-4 w-4 text-blue-600" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{bookings.filter((b) => b.status === "completed").length}</div>
              <p className="text-xs text-muted-foreground">
                {language === "vi" ? "Hoàn thành" : "Successfully completed"}
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content */}
        <Tabs defaultValue="bookings" className="space-y-4">
          <TabsList>
            <TabsTrigger value="bookings">{currentLang.myBookings}</TabsTrigger>
            <TabsTrigger value="new-booking">{currentLang.newBooking}</TabsTrigger>
            {userRole === "admin" && (
              <>
                <TabsTrigger value="approval">{currentLang.approval}</TabsTrigger>
                <TabsTrigger value="equipment">{currentLang.equipment}</TabsTrigger>
                <TabsTrigger value="rooms">{currentLang.rooms}</TabsTrigger>
                <TabsTrigger value="users">{currentLang.users}</TabsTrigger>
              </>
            )}
            <TabsTrigger value="ai-chat">{currentLang.aiAssistant}</TabsTrigger>
          </TabsList>

          <TabsContent value="bookings" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>{currentLang.myBookings}</CardTitle>
                <CardDescription>
                  {language === "vi" ? "Quản lý các lịch đặt thiết bị của bạn" : "Manage your equipment bookings"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  {filteredBookings.map((booking) => (
                    <div key={booking.id} className="flex items-center justify-between p-4 border rounded-lg">
                      <div className="flex-1">
                        <h3 className="font-semibold">{booking.equipment}</h3>
                        <p className="text-sm text-gray-600">
                          {booking.department} - {booking.room}
                        </p>
                        <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                          <span>📅 {booking.date}</span>
                          <span>
                            ⏰ {booking.pickupTime} - {booking.returnTime}
                          </span>
                        </div>
                        {booking.purpose && (
                          <p className="text-sm text-gray-600 mt-1">
                            {currentLang.purpose}: {booking.purpose}
                          </p>
                        )}
                      </div>
                      <div className="flex items-center space-x-2">
                        {getStatusBadge(booking.status)}
                        <Button variant="outline" size="sm" onClick={() => showBookingDetailsModal(booking)}>
                          {currentLang.details}
                        </Button>
                      </div>
                    </div>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="new-booking" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>{currentLang.newBooking}</CardTitle>
                <CardDescription>
                  {language === "vi"
                    ? "Đặt lịch sử dụng thiết bị với AI assistant"
                    : "Book equipment with AI assistant"}
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <Label htmlFor="department">{currentLang.selectDepartment}</Label>
                    <Select
                      value={newBooking.department}
                      onValueChange={(value) =>
                        setNewBooking((prev) => ({ ...prev, department: value, room: "", equipment: "" }))
                      }
                    >
                      <SelectTrigger>
                        <SelectValue placeholder={currentLang.selectDepartment} />
                      </SelectTrigger>
                      <SelectContent>
                        {departments.map((dept) => (
                          <SelectItem key={dept.id} value={dept.name}>
                            {dept.name}
                          </SelectItem>
                        ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="room">{currentLang.selectRoom}</Label>
                    <Select
                      value={newBooking.room}
                      onValueChange={(value) => setNewBooking((prev) => ({ ...prev, room: value, equipment: "" }))}
                      disabled={!newBooking.department}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder={currentLang.selectRoom} />
                      </SelectTrigger>
                      <SelectContent>
                        {departments
                          .find((d) => d.name === newBooking.department)
                          ?.rooms.map((room) => (
                            <SelectItem key={room} value={room}>
                              {room}
                            </SelectItem>
                          ))}
                      </SelectContent>
                    </Select>
                  </div>

                  <div>
                    <Label htmlFor="equipment">{currentLang.selectEquipment}</Label>
                    <Select
                      value={newBooking.equipment}
                      onValueChange={(value) => setNewBooking((prev) => ({ ...prev, equipment: value }))}
                      disabled={!newBooking.department}
                    >
                      <SelectTrigger>
                        <SelectValue placeholder={currentLang.selectEquipment} />
                      </SelectTrigger>
                      <SelectContent>
                        {equipment
                          .filter(
                            (eq) =>
                              eq.department === newBooking.department && eq.available > 0 && eq.status === "available",
                          )
                          .map((eq) => (
                            <SelectItem key={eq.id} value={eq.name}>
                              {eq.name} - {eq.room} ({eq.available}/{eq.quantity}{" "}
                              {language === "vi" ? "có sẵn" : "available"})
                            </SelectItem>
                          ))}
                      </SelectContent>
                    </Select>
                    {newBooking.department && (
                      <p className="text-sm text-muted-foreground mt-1">
                        {language === "vi"
                          ? `Có ${equipment.filter((eq) => eq.department === newBooking.department && eq.available > 0).length} thiết bị có sẵn trong khoa này`
                          : `${equipment.filter((eq) => eq.department === newBooking.department && eq.available > 0).length} equipment available in this department`}
                      </p>
                    )}
                  </div>

                  <div>
                    <Label htmlFor="date">{currentLang.date}</Label>
                    <Input
                      type="date"
                      value={newBooking.date}
                      onChange={(e) => setNewBooking((prev) => ({ ...prev, date: e.target.value }))}
                    />
                  </div>

                  <div>
                    <Label htmlFor="pickupTime">{currentLang.pickupTime}</Label>
                    <Input
                      type="time"
                      value={newBooking.pickupTime}
                      onChange={(e) => setNewBooking((prev) => ({ ...prev, pickupTime: e.target.value }))}
                    />
                  </div>

                  <div>
                    <Label htmlFor="returnTime">{currentLang.returnTime}</Label>
                    <Input
                      type="time"
                      value={newBooking.returnTime}
                      onChange={(e) => setNewBooking((prev) => ({ ...prev, returnTime: e.target.value }))}
                    />
                  </div>
                </div>

                <div>
                  <Label htmlFor="purpose">{currentLang.purpose}</Label>
                  <Textarea
                    placeholder={
                      language === "vi"
                        ? "Mô tả mục đích sử dụng thiết bị..."
                        : "Describe the purpose of equipment usage..."
                    }
                    value={newBooking.purpose}
                    onChange={(e) => setNewBooking((prev) => ({ ...prev, purpose: e.target.value }))}
                  />
                </div>

                <Button onClick={handleBookingSubmit} className="w-full">
                  <BookOpen className="w-4 h-4 mr-2" />
                  {currentLang.bookNow}
                </Button>
              </CardContent>
            </Card>
          </TabsContent>

          {userRole === "admin" && (
            <TabsContent value="equipment" className="space-y-4">
              <Card>
                <CardHeader>
                  <CardTitle>{currentLang.equipment}</CardTitle>
                  <CardDescription>
                    {language === "vi" ? "Quản lý thiết bị phòng lab với AI" : "Manage lab equipment with AI"}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="space-y-4">
                    {equipment.map((eq) => (
                      <div key={eq.id} className="flex items-center justify-between p-4 border rounded-lg">
                        <div className="flex-1">
                          <h3 className="font-semibold">{eq.name}</h3>
                          <p className="text-sm text-gray-600">
                            {eq.department} - {eq.room}
                          </p>
                          {eq.description && <p className="text-xs text-gray-500 mt-1">{eq.description}</p>}
                        </div>
                        <div className="flex items-center space-x-2">
                          <Badge variant={eq.available > 0 ? "default" : "secondary"}>
                            {eq.available > 0
                              ? `${currentLang.available} (${eq.available}/${eq.quantity})`
                              : currentLang.inUse}
                          </Badge>
                          <Button variant="outline" size="sm" onClick={() => editEquipment(eq)}>
                            <Edit className="w-4 h-4 mr-1" />
                            {currentLang.edit}
                          </Button>
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          )}

          {userRole === "admin" && (
            <>
              <TabsContent value="approval" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>{currentLang.approval}</CardTitle>
                    <CardDescription>
                      {language === "vi"
                        ? "Xét duyệt đơn đặt lịch với AI hỗ trợ"
                        : "Review booking requests with AI assistance"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {bookings
                        .filter((booking) => booking.status === "pending")
                        .map((booking) => (
                          <div key={booking.id} className="p-4 border rounded-lg bg-yellow-50">
                            <div className="flex justify-between items-start">
                              <div className="flex-1">
                                <h3 className="font-semibold">{booking.equipment}</h3>
                                <p className="text-sm text-gray-600">
                                  {booking.studentName} ({booking.studentEmail})
                                </p>
                                <p className="text-sm text-gray-600">
                                  {booking.department} - {booking.room}
                                </p>
                                <div className="flex items-center space-x-4 mt-2 text-sm text-gray-500">
                                  <span>📅 {booking.date}</span>
                                  <span>
                                    ⏰ {booking.pickupTime} - {booking.returnTime}
                                  </span>
                                </div>
                                {booking.purpose && (
                                  <p className="text-sm text-gray-600 mt-2">
                                    <strong>{currentLang.purpose}:</strong> {booking.purpose}
                                  </p>
                                )}
                                {booking.aiRisk && (
                                  <div className="mt-2 p-2 bg-blue-50 rounded text-xs">
                                    <strong>AI Risk Assessment:</strong>
                                    <p>Level: {booking.aiRisk.level}</p>
                                    <p>Recommendation: {booking.aiRisk.recommendation}</p>
                                    {booking.aiRisk.issues.length > 0 && (
                                      <p>Issues: {booking.aiRisk.issues.join(", ")}</p>
                                    )}
                                  </div>
                                )}
                              </div>
                              <div className="flex space-x-2 ml-4">
                                <Button
                                  size="sm"
                                  onClick={() => handleApproval(booking.id, "approve")}
                                  className="bg-green-600 hover:bg-green-700"
                                >
                                  <CheckCircle className="w-4 h-4 mr-1" />
                                  {currentLang.approve}
                                </Button>
                                <Button
                                  size="sm"
                                  variant="destructive"
                                  onClick={() => handleApproval(booking.id, "reject")}
                                >
                                  <XCircle className="w-4 h-4 mr-1" />
                                  {currentLang.reject}
                                </Button>
                              </div>
                            </div>
                          </div>
                        ))}
                      {bookings.filter((booking) => booking.status === "pending").length === 0 && (
                        <p className="text-center text-gray-500 py-8">
                          {language === "vi" ? "Không có đơn nào cần xét duyệt" : "No pending requests"}
                        </p>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="rooms" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>{currentLang.rooms}</CardTitle>
                    <CardDescription>
                      {language === "vi" ? "Quản lý phòng lab và thiết bị" : "Manage lab rooms and equipment"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-6">
                      {departments.map((dept) => (
                        <div key={dept.id} className="border rounded-lg p-4">
                          <h3 className="font-semibold text-lg mb-3">{dept.name}</h3>
                          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                            {dept.rooms.map((room) => {
                              const roomEquipment = equipment.filter((eq) => eq.room === room)
                              return (
                                <div key={room} className="p-3 bg-gray-50 rounded">
                                  <h4 className="font-medium">{room}</h4>
                                  <p className="text-sm text-gray-600 mt-1">
                                    {roomEquipment.length} {language === "vi" ? "thiết bị" : "equipment"}
                                  </p>
                                  <p className="text-xs text-green-600">
                                    {roomEquipment.filter((eq) => eq.available > 0).length}{" "}
                                    {language === "vi" ? "có sẵn" : "available"}
                                  </p>
                                  <div className="mt-2 space-y-1">
                                    {roomEquipment.slice(0, 2).map((eq) => (
                                      <p key={eq.id} className="text-xs text-gray-500 truncate">
                                        • {eq.name}
                                      </p>
                                    ))}
                                    {roomEquipment.length > 2 && (
                                      <p className="text-xs text-gray-400">
                                        +{roomEquipment.length - 2} {language === "vi" ? "khác" : "more"}
                                      </p>
                                    )}
                                  </div>
                                </div>
                              )
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="users" className="space-y-4">
                <Card>
                  <CardHeader>
                    <CardTitle>{language === "vi" ? "Quản lý người dùng" : "User Management"}</CardTitle>
                    <CardDescription>
                      {language === "vi"
                        ? "Quản lý tài khoản người dùng trong hệ thống"
                        : "Manage user accounts in the system"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="space-y-4">
                      {users.map((userData) => (
                        <div key={userData.id} className="flex items-center justify-between p-4 border rounded-lg">
                          <div className="flex-1">
                            <div className="flex items-center space-x-4">
                              <div className="flex-1">
                                <h3 className="font-medium">{userData.name}</h3>
                                <p className="text-sm text-gray-600">{userData.email}</p>
                                <p className="text-xs text-gray-500">
                                  {userData.role === "admin"
                                    ? language === "vi"
                                      ? "Quản trị viên"
                                      : "Administrator"
                                    : userData.role === "teacher"
                                      ? language === "vi"
                                        ? "Giảng viên"
                                        : "Teacher"
                                      : language === "vi"
                                        ? "Sinh viên"
                                        : "Student"}{" "}
                                  • {userData.department}
                                </p>
                              </div>
                              <div className="flex items-center space-x-2">
                                <Badge variant={userData.status === "active" ? "default" : "secondary"}>
                                  {userData.status === "active"
                                    ? language === "vi"
                                      ? "Hoạt động"
                                      : "Active"
                                    : language === "vi"
                                      ? "Tạm khóa"
                                      : "Inactive"}
                                </Badge>
                              </div>
                            </div>
                          </div>
                          <div className="flex space-x-2">
                            <Button variant="outline" size="sm" onClick={() => editUser(userData)}>
                              <Edit className="w-4 h-4 mr-1" />
                              {language === "vi" ? "Sửa" : "Edit"}
                            </Button>
                            <Button
                              variant={userData.status === "active" ? "destructive" : "default"}
                              size="sm"
                              onClick={() => toggleUserStatus(userData.id)}
                            >
                              {userData.status === "active"
                                ? language === "vi"
                                  ? "Khóa"
                                  : "Deactivate"
                                : language === "vi"
                                  ? "Kích hoạt"
                                  : "Activate"}
                            </Button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>
            </>
          )}

          <TabsContent value="ai-chat" className="space-y-4">
            <Card>
              <CardHeader>
                <CardTitle>{currentLang.aiAssistant}</CardTitle>
                <CardDescription>
                  {language === "vi"
                    ? "Trợ lý AI thông minh - hỗ trợ đặt lịch, tìm kiếm thiết bị và trả lời mọi câu hỏi"
                    : "Smart AI Assistant - booking support, equipment search, and general Q&A"}
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div className="h-96 overflow-y-auto border rounded-lg p-4 bg-gray-50">
                    {chatMessages.map((message, index) => (
                      <div key={index} className={`mb-4 ${message.role === "user" ? "text-right" : "text-left"}`}>
                        <div
                          className={`inline-block max-w-xs lg:max-w-md px-4 py-2 rounded-lg ${
                            message.role === "user" ? "bg-blue-600 text-white" : "bg-white border"
                          }`}
                        >
                          <p className="text-sm">{message.content}</p>
                        </div>
                      </div>
                    ))}
                  </div>
                  <div className="flex space-x-2">
                    <Input
                      placeholder={currentLang.askAI}
                      value={chatInput}
                      onChange={(e) => setChatInput(e.target.value)}
                      onKeyPress={(e) => e.key === "Enter" && handleChatSubmit()}
                      className="flex-1"
                    />
                    <Button onClick={handleChatSubmit}>{currentLang.send}</Button>
                  </div>
                  <div className="text-xs text-gray-500 space-y-1">
                    <p>
                      <strong>{language === "vi" ? "Ví dụ câu hỏi:" : "Example questions:"}</strong>
                    </p>
                    <p>
                      •{" "}
                      {language === "vi"
                        ? "Tôi cần mượn máy ly tâm vào thứ 2"
                        : "I need to borrow a centrifuge on Monday"}
                    </p>
                    <p>
                      •{" "}
                      {language === "vi"
                        ? "Khoa Sinh học có những thiết bị gì?"
                        : "What equipment does Biology department have?"}
                    </p>
                    <p>• {language === "vi" ? "Cách sử dụng máy PCR như thế nào?" : "How to use PCR machine?"}</p>
                    <p>• {language === "vi" ? "Thời tiết hôm nay thế nào?" : "What's the weather today?"}</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>

        <Dialog open={showBookingDetails} onOpenChange={setShowBookingDetails}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>{currentLang.bookingDetails}</DialogTitle>
            </DialogHeader>
            {selectedBooking && (
              <div className="space-y-4">
                <div>
                  <h3 className="font-semibold text-lg">{selectedBooking.equipment}</h3>
                  <p className="text-gray-600">
                    {selectedBooking.department} - {selectedBooking.room}
                  </p>
                </div>

                <div className="grid grid-cols-2 gap-4 text-sm">
                  <div>
                    <strong>{currentLang.date}:</strong>
                    <p>{selectedBooking.date}</p>
                  </div>
                  <div>
                    <strong>{currentLang.status}:</strong>
                    <div className="mt-1">{getStatusBadge(selectedBooking.status)}</div>
                  </div>
                  <div>
                    <strong>{currentLang.pickupTime}:</strong>
                    <p>{selectedBooking.pickupTime}</p>
                  </div>
                  <div>
                    <strong>{currentLang.returnTime}:</strong>
                    <p>{selectedBooking.returnTime}</p>
                  </div>
                </div>

                {selectedBooking.purpose && (
                  <div>
                    <strong>{currentLang.purpose}:</strong>
                    <p className="text-sm text-gray-600 mt-1">{selectedBooking.purpose}</p>
                  </div>
                )}

                {userRole === "admin" && (
                  <div>
                    <strong>{language === "vi" ? "Sinh viên:" : "Student:"}:</strong>
                    <p className="text-sm">
                      {selectedBooking.studentName} ({selectedBooking.studentEmail})
                    </p>
                  </div>
                )}
              </div>
            )}
          </DialogContent>
        </Dialog>

        <Dialog open={showEquipmentEdit} onOpenChange={setShowEquipmentEdit}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>{currentLang.editEquipment}</DialogTitle>
            </DialogHeader>
            {editingEquipment && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="equipmentName">{currentLang.equipmentName}</Label>
                  <Input
                    value={editingEquipment.name}
                    onChange={(e) => setEditingEquipment((prev) => ({ ...prev, name: e.target.value }))}
                  />
                </div>

                <div>
                  <Label htmlFor="description">{currentLang.description}</Label>
                  <Textarea
                    value={editingEquipment.description || ""}
                    onChange={(e) => setEditingEquipment((prev) => ({ ...prev, description: e.target.value }))}
                  />
                </div>

                <div>
                  <Label htmlFor="specifications">{currentLang.specifications}</Label>
                  <Textarea
                    value={editingEquipment.specifications || ""}
                    onChange={(e) => setEditingEquipment((prev) => ({ ...prev, specifications: e.target.value }))}
                  />
                </div>

                <div className="space-y-2">
                  <Label>Số lượng có sẵn</Label>
                  <Input
                    type="number"
                    min="0"
                    max={editingEquipment.quantity}
                    value={editingEquipment.available}
                    onChange={(e) =>
                      setEditingEquipment((prev) => ({ ...prev, available: Number.parseInt(e.target.value) || 0 }))
                    }
                  />
                </div>

                <div className="space-y-2">
                  <Label>Tổng số lượng</Label>
                  <Input
                    type="number"
                    min="1"
                    value={editingEquipment.quantity}
                    onChange={(e) =>
                      setEditingEquipment((prev) => ({ ...prev, quantity: Number.parseInt(e.target.value) || 1 }))
                    }
                  />
                </div>

                <div className="flex space-x-2">
                  <Button onClick={saveEquipmentChanges} className="flex-1">
                    {currentLang.save}
                  </Button>
                  <Button variant="outline" onClick={() => setShowEquipmentEdit(false)} className="flex-1">
                    {currentLang.cancel}
                  </Button>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>

        <Dialog open={showUserEdit} onOpenChange={setShowUserEdit}>
          <DialogContent className="max-w-md">
            <DialogHeader>
              <DialogTitle>{language === "vi" ? "Chỉnh sửa người dùng" : "Edit User"}</DialogTitle>
            </DialogHeader>
            {editingUser && (
              <div className="space-y-4">
                <div>
                  <Label htmlFor="userName">{language === "vi" ? "Họ tên" : "Full Name"}</Label>
                  <Input
                    value={editingUser.name}
                    onChange={(e) => setEditingUser((prev) => ({ ...prev, name: e.target.value }))}
                  />
                </div>

                <div>
                  <Label htmlFor="userEmail">Email</Label>
                  <Input
                    value={editingUser.email}
                    onChange={(e) => setEditingUser((prev) => ({ ...prev, email: e.target.value }))}
                  />
                </div>

                <div>
                  <Label htmlFor="userRole">{language === "vi" ? "Vai trò" : "Role"}</Label>
                  <select
                    className="w-full p-2 border rounded"
                    value={editingUser.role}
                    onChange={(e) => setEditingUser((prev) => ({ ...prev, role: e.target.value }))}
                  >
                    <option value="student">{language === "vi" ? "Sinh viên" : "Student"}</option>
                    <option value="teacher">{language === "vi" ? "Giảng viên" : "Teacher"}</option>
                    <option value="admin">{language === "vi" ? "Quản trị viên" : "Administrator"}</option>
                  </select>
                </div>

                <div>
                  <Label htmlFor="userDepartment">{language === "vi" ? "Khoa" : "Department"}</Label>
                  <select
                    className="w-full p-2 border rounded"
                    value={editingUser.department}
                    onChange={(e) => setEditingUser((prev) => ({ ...prev, department: e.target.value }))}
                  >
                    {departments.map((dept) => (
                      <option key={dept.id} value={dept.name}>
                        {dept.name}
                      </option>
                    ))}
                  </select>
                </div>

                <div className="flex space-x-2">
                  <Button onClick={saveUserChanges} className="flex-1">
                    {language === "vi" ? "Lưu" : "Save"}
                  </Button>
                  <Button variant="outline" onClick={() => setShowUserEdit(false)} className="flex-1">
                    {language === "vi" ? "Hủy" : "Cancel"}
                  </Button>
                </div>
              </div>
            )}
          </DialogContent>
        </Dialog>
      </div>
    </div>
  )
}
