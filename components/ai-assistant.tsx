"use client"

import type React from "react"
import { useState, useContext } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Textarea } from "@/components/ui/textarea"
import { Badge } from "@/components/ui/badge"
import { Sparkles, Send, Bot, User } from "lucide-react"
import { AppContext } from "./app-context"

interface Message {
  id: string
  role: "user" | "assistant"
  content: string
  timestamp: Date
  actions?: Array<{
    label: string
    action: () => void
  }>
}

interface AIAssistantProps {
  language: "vi" | "en"
  onNavigate?: (section: string) => void
}

export function AIAssistant({ language, onNavigate }: AIAssistantProps) {
  const { equipment, bookings, addBooking } = useContext(AppContext)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [isLoading, setIsLoading] = useState(false)

  const getSmartResponse = (
    question: string,
  ): { content: string; actions?: Array<{ label: string; action: () => void }> } => {
    const q = question.toLowerCase()

    // Câu hỏi về thiết bị theo khoa
    if (q.includes("khoa") && (q.includes("thiết bị") || q.includes("máy"))) {
      const departments = ["Khoa Sinh học", "Khoa Vật lý", "Khoa Hóa học", "Khoa Công nghệ thông tin"]
      let response = "📋 **Danh sách thiết bị theo khoa:**\n\n"

      departments.forEach((dept) => {
        const deptEquipment = equipment.filter((eq) => eq.department === dept)
        response += `**${dept}:**\n`
        deptEquipment.forEach((eq) => {
          response += `• ${eq.name} - ${eq.room} (${eq.available}/${eq.total} có sẵn)\n`
        })
        response += "\n"
      })

      return {
        content: response,
        actions: [
          {
            label: "Đặt lịch ngay",
            action: () => onNavigate?.("booking"),
          },
        ],
      }
    }

    // Câu hỏi về thiết bị cụ thể
    if (q.includes("máy ly tâm") || q.includes("centrifuge")) {
      const centrifuge = equipment.find((eq) => eq.name.includes("Centrifuge"))
      if (centrifuge) {
        return {
          content: `🔬 **Máy ly tâm Centrifuge CF-15**\n\n📍 Vị trí: ${centrifuge.room}\n📊 Trạng thái: ${centrifuge.available}/${centrifuge.total} có sẵn\n🏢 Khoa: ${centrifuge.department}\n\n💡 **Cách sử dụng:**\n• Kiểm tra cân bằng mẫu trước khi chạy\n• Đặt tốc độ phù hợp (thường 3000-15000 rpm)\n• Thời gian ly tâm: 5-30 phút tùy mẫu\n• Luôn đóng nắp trước khi khởi động`,
          actions: [
            {
              label: "Đặt lịch máy ly tâm",
              action: () => {
                const booking = {
                  id: Date.now().toString(),
                  userId: "current-user",
                  userName: "Sinh viên",
                  equipmentId: centrifuge.id,
                  equipmentName: centrifuge.name,
                  room: centrifuge.room,
                  date: new Date().toISOString().split("T")[0],
                  startTime: "09:00",
                  endTime: "11:00",
                  purpose: "Ly tâm mẫu sinh học",
                  status: "pending" as const,
                  createdAt: new Date(),
                }
                addBooking(booking)
                setMessages((prev) => [
                  ...prev,
                  {
                    id: Date.now().toString(),
                    role: "assistant",
                    content: "✅ Đã tạo booking máy ly tâm thành công! Vui lòng kiểm tra tab 'Lịch đặt của tôi'.",
                    timestamp: new Date(),
                  },
                ])
              },
            },
          ],
        }
      }
    }

    // Câu hỏi về PCR
    if (q.includes("pcr")) {
      return {
        content: `🧬 **Máy PCR Thermal Cycler**\n\n📍 Vị trí: Lab B101\n📊 Trạng thái: Có sẵn\n🏢 Khoa: Sinh học\n\n💡 **Hướng dẫn sử dụng PCR:**\n\n**1. Chuẩn bị mẫu:**\n• DNA template: 10-100 ng\n• Primer forward/reverse: 0.2-1 μM\n• dNTPs: 200 μM mỗi loại\n• Taq polymerase: 1-2.5 units\n• Buffer: 1x\n\n**2. Chu trình nhiệt độ:**\n• Denaturation: 94°C - 30s\n• Annealing: 55-65°C - 30s\n• Extension: 72°C - 1 phút/kb\n• Số chu kỳ: 25-35\n\n**3. Lưu ý an toàn:**\n• Đeo găng tay và kính bảo hộ\n• Làm việc trong tủ hút\n• Xử lý chất thải đúng quy định`,
      }
    }

    // Câu hỏi về booking/đặt lịch
    if (q.includes("đặt lịch") || q.includes("booking")) {
      const pendingBookings = bookings.filter((b) => b.status === "pending").length
      const approvedBookings = bookings.filter((b) => b.status === "approved").length

      return {
        content: `📅 **Thông tin đặt lịch hiện tại:**\n\n• Tổng số booking: ${bookings.length}\n• Đang chờ duyệt: ${pendingBookings}\n• Đã được duyệt: ${approvedBookings}\n\n💡 **Hướng dẫn đặt lịch:**\n1. Chọn khoa và thiết bị\n2. Chọn ngày và giờ sử dụng\n3. Mô tả mục đích sử dụng\n4. Gửi yêu cầu và chờ admin duyệt`,
        actions: [
          {
            label: "Tạo booking mới",
            action: () => onNavigate?.("booking"),
          },
          {
            label: "Xem lịch của tôi",
            action: () => onNavigate?.("my-bookings"),
          },
        ],
      }
    }

    // Câu hỏi về thống kê
    if (q.includes("thống kê") || q.includes("báo cáo")) {
      const totalEquipment = equipment.length
      const availableEquipment = equipment.filter((eq) => eq.available > 0).length
      const busyEquipment = equipment.filter((eq) => eq.available === 0).length

      return {
        content: `📊 **Thống kê hệ thống:**\n\n🔧 **Thiết bị:**\n• Tổng số: ${totalEquipment}\n• Có sẵn: ${availableEquipment}\n• Đang sử dụng: ${busyEquipment}\n\n📅 **Booking:**\n• Tổng số: ${bookings.length}\n• Chờ duyệt: ${bookings.filter((b) => b.status === "pending").length}\n• Đã duyệt: ${bookings.filter((b) => b.status === "approved").length}\n• Từ chối: ${bookings.filter((b) => b.status === "rejected").length}`,
        actions: [
          {
            label: "Xem chi tiết thiết bị",
            action: () => onNavigate?.("equipment"),
          },
        ],
      }
    }

    // Câu hỏi chung về khoa học
    if (q.includes("dna") || q.includes("protein") || q.includes("enzyme")) {
      return {
        content: `🧬 **Kiến thức sinh học phân tử:**\n\n**DNA (Deoxyribonucleic Acid):**\n• Cấu trúc: Chuỗi kép xoắn\n• Thành phần: A, T, G, C\n• Chức năng: Lưu trữ thông tin di truyền\n\n**Protein:**\n• Cấu trúc: Chuỗi amino acid\n• Chức năng: Enzyme, cấu trúc, vận chuyển\n• Tổng hợp: Từ mRNA qua ribosome\n\n**Enzyme:**\n• Bản chất: Protein xúc tác\n• Đặc tính: Đặc hiệu, bị ảnh hưởng bởi pH, nhiệt độ\n• Ứng dụng: PCR, cắt DNA, nối DNA`,
      }
    }

    // Câu hỏi về hóa học
    if (q.includes("ph") || q.includes("acid") || q.includes("base")) {
      return {
        content: `⚗️ **Kiến thức hóa học cơ bản:**\n\n**pH (Potential of Hydrogen):**\n• Thang đo: 0-14\n• pH < 7: Acid\n• pH = 7: Trung tính\n• pH > 7: Base\n\n**Acid mạnh:** HCl, H₂SO₄, HNO₃\n**Base mạnh:** NaOH, KOH, Ca(OH)₂\n\n**Ứng dụng trong lab:**\n• Điều chỉnh pH dung dịch\n• Chuẩn độ acid-base\n• Bảo quản mẫu sinh học`,
      }
    }

    // Câu hỏi về vật lý
    if (q.includes("quang phổ") || q.includes("uv") || q.includes("spectroscopy")) {
      return {
        content: `🔬 **Quang phổ học:**\n\n**UV-Vis Spectroscopy:**\n• Nguyên lý: Hấp thụ ánh sáng UV-Vis\n• Ứng dụng: Định lượng protein, DNA\n• Bước sóng: 200-800 nm\n\n**Định luật Beer-Lambert:**\n• A = εcl\n• A: Độ hấp thụ\n• ε: Hệ số hấp thụ\n• c: Nồng độ\n• l: Độ dài quang học\n\n**Máy quang phổ UV-Vis có sẵn tại Lab C301**`,
      }
    }

    // Trả lời mặc định thông minh
    return {
      content: `🤖 Tôi là AI Assistant của hệ thống quản lý Lab DNU!\n\n💡 **Tôi có thể giúp bạn:**\n• Thông tin thiết bị và khoa\n• Hướng dẫn sử dụng máy móc\n• Kiến thức khoa học (Sinh, Lý, Hóa, CNTT)\n• Đặt lịch và quản lý booking\n• Thống kê và báo cáo\n\n❓ **Hãy thử hỏi:**\n• "Khoa Sinh học có những thiết bị gì?"\n• "Cách sử dụng máy PCR như thế nào?"\n• "Tôi muốn đặt lịch máy ly tâm"\n• "DNA là gì?"\n• "Thống kê hệ thống hiện tại"`,
      actions: [
        {
          label: "Xem thiết bị",
          action: () => onNavigate?.("equipment"),
        },
        {
          label: "Đặt lịch mới",
          action: () => onNavigate?.("booking"),
        },
      ],
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim()) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: "user",
      content: input,
      timestamp: new Date(),
    }

    setMessages((prev) => [...prev, userMessage])
    const currentInput = input
    setInput("")
    setIsLoading(true)

    setTimeout(() => {
      const response = getSmartResponse(currentInput)
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: "assistant",
        content: response.content,
        timestamp: new Date(),
        actions: response.actions,
      }

      setMessages((prev) => [...prev, assistantMessage])
      setIsLoading(false)
    }, 1000)
  }

  const suggestedQuestions = [
    "Khoa Sinh học có những thiết bị gì?",
    "Cách sử dụng máy PCR như thế nào?",
    "Tôi cần mượn máy ly tâm vào thứ 2",
    "DNA là gì?",
    "Thống kê hệ thống hiện tại",
  ]

  return (
    <Card className="h-[600px] flex flex-col">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Sparkles className="h-5 w-5 text-orange-500" />
          {language === "vi" ? "Trợ lý AI" : "AI Assistant"}
          <Badge variant="secondary" className="bg-orange-100 text-orange-700">
            DNU Lab AI
          </Badge>
        </CardTitle>
        <p className="text-sm text-muted-foreground">
          {language === "vi"
            ? "Trợ lý AI thông minh - hỗ trợ đặt lịch, tìm kiếm thiết bị và trả lời mọi câu hỏi"
            : "Smart AI Assistant - booking support, equipment search and Q&A"}
        </p>
      </CardHeader>

      <CardContent className="flex-1 flex flex-col">
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.length === 0 && (
            <div className="text-center text-muted-foreground py-4">
              <Bot className="h-12 w-12 mx-auto mb-4 text-orange-500" />
              <p className="mb-4">
                {language === "vi"
                  ? "Xin chào! Tôi là AI Assistant siêu thông minh của DNU Lab! 🚀"
                  : "Hello! I'm the super smart AI Assistant of DNU Lab! 🚀"}
              </p>

              <div className="text-left max-w-md mx-auto">
                <p className="font-medium mb-2">Ví dụ câu hỏi:</p>
                <div className="space-y-1">
                  {suggestedQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => setInput(question)}
                      className="block w-full text-left text-sm p-2 rounded bg-orange-50 hover:bg-orange-100 text-orange-700 transition-colors"
                    >
                      • {question}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          )}

          {messages.map((message) => (
            <div key={message.id} className={`flex gap-3 ${message.role === "user" ? "justify-end" : "justify-start"}`}>
              <div className={`flex gap-2 max-w-[85%] ${message.role === "user" ? "flex-row-reverse" : "flex-row"}`}>
                <div
                  className={`w-8 h-8 rounded-full flex items-center justify-center ${
                    message.role === "user" ? "bg-orange-500" : "bg-blue-500"
                  }`}
                >
                  {message.role === "user" ? (
                    <User className="h-4 w-4 text-white" />
                  ) : (
                    <Bot className="h-4 w-4 text-white" />
                  )}
                </div>
                <div
                  className={`rounded-lg p-3 ${
                    message.role === "user" ? "bg-orange-500 text-white" : "bg-gray-100 text-gray-900 border"
                  }`}
                >
                  <div className="whitespace-pre-wrap">{message.content}</div>

                  {message.actions && message.actions.length > 0 && (
                    <div className="mt-3 space-y-2">
                      {message.actions.map((action, index) => (
                        <Button
                          key={index}
                          size="sm"
                          variant="outline"
                          onClick={action.action}
                          className="mr-2 bg-white hover:bg-orange-50 border-orange-200"
                        >
                          {action.label}
                        </Button>
                      ))}
                    </div>
                  )}

                  <p className="text-xs opacity-70 mt-2">{message.timestamp.toLocaleTimeString()}</p>
                </div>
              </div>
            </div>
          ))}

          {isLoading && (
            <div className="flex gap-3">
              <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center">
                <Bot className="h-4 w-4 text-white" />
              </div>
              <div className="bg-gray-100 rounded-lg p-3 border">
                <div className="flex space-x-1">
                  <div className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"></div>
                  <div
                    className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.1s" }}
                  ></div>
                  <div
                    className="w-2 h-2 bg-orange-400 rounded-full animate-bounce"
                    style={{ animationDelay: "0.2s" }}
                  ></div>
                </div>
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="flex gap-2">
          <Textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder={language === "vi" ? "Hỏi AI..." : "Ask AI..."}
            className="flex-1 min-h-[40px] max-h-[120px] resize-none"
            onKeyDown={(e) => {
              if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault()
                handleSubmit(e)
              }
            }}
          />
          <Button
            type="submit"
            disabled={isLoading || !input.trim()}
            className="bg-orange-500 hover:bg-orange-600 text-white"
          >
            <Send className="h-4 w-4" />
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
