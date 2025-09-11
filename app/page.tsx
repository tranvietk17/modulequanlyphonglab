"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Badge } from "@/components/ui/badge"
import { Globe, BookOpen, Calendar, MessageCircle, ChevronRight, User, Shield } from "lucide-react"
import { Dashboard } from "@/components/dashboard"
import { AppProvider, useAppContext } from "@/components/app-context"

function HomePage() {
  const [language, setLanguage] = useState<"vi" | "en">("vi")
  const [showChat, setShowChat] = useState(false)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [currentUser, setCurrentUser] = useState<{ role: "student" | "admin"; name: string; email: string } | null>(
    null,
  )
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  const [regFullName, setRegFullName] = useState("")
  const [regStudentId, setRegStudentId] = useState("")
  const [regDepartment, setRegDepartment] = useState("")
  const [regEmail, setRegEmail] = useState("")
  const [regPassword, setRegPassword] = useState("")

  const { getUserByEmail, addUser } = useAppContext()

  const demoAccounts = {
    student: {
      email: "student@dnu.edu.vn",
      password: "student123",
      name: "Nguyễn Văn A",
      role: "student" as const,
    },
    admin: {
      email: "admin@dnu.edu.vn",
      password: "admin123",
      name: "Trần Thị B",
      role: "admin" as const,
    },
  }

  const handleLogin = () => {
    const studentAccount = demoAccounts.student
    const adminAccount = demoAccounts.admin

    if (loginEmail === studentAccount.email && loginPassword === studentAccount.password) {
      setCurrentUser({ role: studentAccount.role, name: studentAccount.name, email: studentAccount.email })
      setIsLoggedIn(true)
    } else if (loginEmail === adminAccount.email && loginPassword === adminAccount.password) {
      setCurrentUser({ role: adminAccount.role, name: adminAccount.name, email: adminAccount.email })
      setIsLoggedIn(true)
    } else {
      const user = getUserByEmail(loginEmail)
      if (user && loginPassword === "123456") {
        // Simple password for demo
        setCurrentUser({
          role: user.role as "student" | "admin",
          name: user.name,
          email: user.email,
        })
        setIsLoggedIn(true)
      } else {
        alert(language === "vi" ? "Sai email hoặc mật khẩu!" : "Invalid email or password!")
      }
    }
  }

  const handleRegister = () => {
    if (!regFullName || !regEmail || !regPassword || !regDepartment) {
      alert(language === "vi" ? "Vui lòng điền đầy đủ thông tin!" : "Please fill in all fields!")
      return
    }

    // Check if email already exists
    if (getUserByEmail(regEmail)) {
      alert(language === "vi" ? "Email đã tồn tại!" : "Email already exists!")
      return
    }

    // Add new user
    addUser({
      name: regFullName,
      email: regEmail,
      role: "student",
      department: regDepartment,
      status: "active",
      studentId: regStudentId,
    })

    alert(
      language === "vi"
        ? "Đăng ký thành công! Mật khẩu mặc định: 123456"
        : "Registration successful! Default password: 123456",
    )

    // Clear form
    setRegFullName("")
    setRegStudentId("")
    setRegDepartment("")
    setRegEmail("")
    setRegPassword("")
  }

  const handleLogout = () => {
    setIsLoggedIn(false)
    setCurrentUser(null)
    setLoginEmail("")
    setLoginPassword("")
  }

  const loginAsDemo = (accountType: "student" | "admin") => {
    const account = demoAccounts[accountType]
    setLoginEmail(account.email)
    setLoginPassword(account.password)
    setCurrentUser({ role: account.role, name: account.name, email: account.email })
    setIsLoggedIn(true)
  }

  const t = {
    vi: {
      title: "Hệ Thống Quản Lý Phòng Lab DNU",
      subtitle: "Đặt lịch thiết bị phòng Lab một cách thông minh và hiệu quả",
      login: "Đăng Nhập",
      register: "Đăng Ký",
      email: "Email",
      password: "Mật khẩu",
      fullName: "Họ và tên",
      studentId: "Mã sinh viên",
      department: "Khoa",
      loginBtn: "Đăng nhập",
      registerBtn: "Tạo tài khoản",
      logout: "Đăng xuất",
      demoAccounts: "Tài khoản demo",
      demoStudent: "Đăng nhập sinh viên",
      demoAdmin: "Đăng nhập admin",
      demoNote: "Sử dụng tài khoản demo để trải nghiệm hệ thống",
      features: "Tính năng nổi bật",
      smartBooking: "Đặt lịch thông minh",
      smartBookingDesc: "AI hỗ trợ phân tích và gợi ý thời gian đặt lịch tối ưu",
      equipmentMgmt: "Quản lý thiết bị",
      equipmentMgmtDesc: "Theo dõi trạng thái và lịch sử sử dụng thiết bị chi tiết",
      aiAssistant: "Trợ lý AI",
      aiAssistantDesc: "Chatbot thông minh hỗ trợ 24/7, trả lời mọi thắc mắc",
      multiLang: "Đa ngôn ngữ",
      multiLangDesc: "Hỗ trợ tiếng Việt và tiếng Anh cho người dùng quốc tế",
      chatPlaceholder: "Hỏi tôi về hệ thống lab...",
      send: "Gửi",
    },
    en: {
      title: "DNU Lab Room Management System",
      subtitle: "Smart and efficient laboratory equipment booking system",
      login: "Login",
      register: "Register",
      email: "Email",
      password: "Password",
      fullName: "Full Name",
      studentId: "Student ID",
      department: "Department",
      loginBtn: "Sign In",
      registerBtn: "Create Account",
      logout: "Logout",
      demoAccounts: "Demo Accounts",
      demoStudent: "Login as Student",
      demoAdmin: "Login as Admin",
      demoNote: "Use demo accounts to experience the system",
      features: "Key Features",
      smartBooking: "Smart Booking",
      smartBookingDesc: "AI-powered analysis and optimal booking time suggestions",
      equipmentMgmt: "Equipment Management",
      equipmentMgmtDesc: "Detailed equipment status tracking and usage history",
      aiAssistant: "AI Assistant",
      aiAssistantDesc: "24/7 intelligent chatbot support for all your questions",
      multiLang: "Multi-language",
      multiLangDesc: "Vietnamese and English support for international users",
      chatPlaceholder: "Ask me about the lab system...",
      send: "Send",
    },
  }

  const currentLang = t[language]

  if (isLoggedIn && currentUser) {
    return (
      <div>
        <div className="bg-white shadow-sm border-b">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center h-16">
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-blue-600 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-6 h-6 text-white" />
                </div>
                <h1 className="text-xl font-bold text-gray-900">DNU Lab</h1>
              </div>

              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  {language === "vi" ? "Xin chào" : "Hello"}, {currentUser.name}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setLanguage(language === "vi" ? "en" : "vi")}
                  className="flex items-center space-x-2"
                >
                  <Globe className="w-4 h-4" />
                  <span>{language === "vi" ? "EN" : "VI"}</span>
                </Button>
                <Button variant="outline" onClick={handleLogout}>
                  {currentLang.logout}
                </Button>
              </div>
            </div>
          </div>
        </div>
        <Dashboard userRole={currentUser.role} language={language} currentUserEmail={currentUser.email} />
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-100">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-orange-600 rounded-lg flex items-center justify-center">
                <BookOpen className="w-6 h-6 text-white" />
              </div>
              <h1 className="text-xl font-bold text-gray-900">DNU Lab</h1>
            </div>

            <div className="flex items-center space-x-4">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setLanguage(language === "vi" ? "en" : "vi")}
                className="flex items-center space-x-2"
              >
                <Globe className="w-4 h-4" />
                <span>{language === "vi" ? "EN" : "VI"}</span>
              </Button>

              <Button onClick={() => setShowChat(!showChat)} className="bg-orange-600 hover:bg-orange-700">
                <MessageCircle className="w-4 h-4 mr-2" />
                AI Chat
              </Button>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="py-20 px-4">
        <div className="max-w-4xl mx-auto text-center">
          <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">{currentLang.title}</h1>
          <p className="text-xl text-gray-600 mb-12 max-w-2xl mx-auto">{currentLang.subtitle}</p>

          <div className="mb-8">
            <Card className="max-w-md mx-auto mb-6">
              <CardHeader>
                <CardTitle className="flex items-center justify-center space-x-2">
                  <User className="w-5 h-5" />
                  <span>{currentLang.demoAccounts}</span>
                </CardTitle>
                <CardDescription>{currentLang.demoNote}</CardDescription>
              </CardHeader>
              <CardContent className="space-y-3">
                <Button onClick={() => loginAsDemo("student")} className="w-full bg-green-600 hover:bg-green-700">
                  <User className="w-4 h-4 mr-2" />
                  {currentLang.demoStudent}
                </Button>
                <Button onClick={() => loginAsDemo("admin")} className="w-full bg-purple-600 hover:bg-purple-700">
                  <Shield className="w-4 h-4 mr-2" />
                  {currentLang.demoAdmin}
                </Button>
                <div className="text-xs text-gray-500 space-y-1">
                  <p>👨‍🎓 Student: student@dnu.edu.vn / student123</p>
                  <p>👨‍💼 Admin: admin@dnu.edu.vn / admin123</p>
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Login/Register Forms */}
          <div className="max-w-md mx-auto">
            <Tabs defaultValue="login" className="w-full">
              <TabsList className="grid w-full grid-cols-2">
                <TabsTrigger value="login">{currentLang.login}</TabsTrigger>
                <TabsTrigger value="register">{currentLang.register}</TabsTrigger>
              </TabsList>

              <TabsContent value="login">
                <Card>
                  <CardHeader>
                    <CardTitle>{currentLang.login}</CardTitle>
                    <CardDescription>
                      {language === "vi" ? "Đăng nhập vào tài khoản của bạn" : "Sign in to your account"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="email">{currentLang.email}</Label>
                      <Input
                        id="email"
                        type="email"
                        placeholder="student@dnu.edu.vn"
                        value={loginEmail}
                        onChange={(e) => setLoginEmail(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="password">{currentLang.password}</Label>
                      <Input
                        id="password"
                        type="password"
                        value={loginPassword}
                        onChange={(e) => setLoginPassword(e.target.value)}
                      />
                    </div>
                    <Button onClick={handleLogin} className="w-full bg-orange-600 hover:bg-orange-700">
                      {currentLang.loginBtn}
                      <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="register">
                <Card>
                  <CardHeader>
                    <CardTitle>{currentLang.register}</CardTitle>
                    <CardDescription>
                      {language === "vi" ? "Tạo tài khoản mới" : "Create a new account"}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="space-y-2">
                      <Label htmlFor="fullName">{currentLang.fullName}</Label>
                      <Input
                        id="fullName"
                        placeholder={language === "vi" ? "Nguyễn Văn A" : "John Doe"}
                        value={regFullName}
                        onChange={(e) => setRegFullName(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="studentId">{currentLang.studentId}</Label>
                      <Input
                        id="studentId"
                        placeholder="2024001234"
                        value={regStudentId}
                        onChange={(e) => setRegStudentId(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="department">{currentLang.department}</Label>
                      <Input
                        id="department"
                        placeholder={language === "vi" ? "Công nghệ thông tin" : "Information Technology"}
                        value={regDepartment}
                        onChange={(e) => setRegDepartment(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="regEmail">{currentLang.email}</Label>
                      <Input
                        id="regEmail"
                        type="email"
                        placeholder="student@dnu.edu.vn"
                        value={regEmail}
                        onChange={(e) => setRegEmail(e.target.value)}
                      />
                    </div>
                    <div className="space-y-2">
                      <Label htmlFor="regPassword">{currentLang.password}</Label>
                      <Input
                        id="regPassword"
                        type="password"
                        value={regPassword}
                        onChange={(e) => setRegPassword(e.target.value)}
                      />
                    </div>
                    <Button onClick={handleRegister} className="w-full bg-green-600 hover:bg-green-700">
                      {currentLang.registerBtn}
                      <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                  </CardContent>
                </Card>
              </TabsContent>
            </Tabs>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">{currentLang.features}</h2>
            <p className="text-xl text-gray-600">
              {language === "vi"
                ? "Những tính năng hiện đại giúp quản lý lab hiệu quả"
                : "Modern features for efficient lab management"}
            </p>
          </div>

          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Calendar className="w-12 h-12 text-orange-600 mx-auto mb-4" />
                <CardTitle className="text-lg">{currentLang.smartBooking}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{currentLang.smartBookingDesc}</p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <BookOpen className="w-12 h-12 text-green-600 mx-auto mb-4" />
                <CardTitle className="text-lg">{currentLang.equipmentMgmt}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{currentLang.equipmentMgmtDesc}</p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <MessageCircle className="w-12 h-12 text-purple-600 mx-auto mb-4" />
                <CardTitle className="text-lg">{currentLang.aiAssistant}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{currentLang.aiAssistantDesc}</p>
              </CardContent>
            </Card>

            <Card className="text-center hover:shadow-lg transition-shadow">
              <CardHeader>
                <Globe className="w-12 h-12 text-orange-600 mx-auto mb-4" />
                <CardTitle className="text-lg">{currentLang.multiLang}</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-600">{currentLang.multiLangDesc}</p>
              </CardContent>
            </Card>
          </div>
        </div>
      </section>

      {/* AI Chat Widget */}
      {showChat && (
        <div className="fixed bottom-4 right-4 w-80 h-96 bg-white rounded-lg shadow-2xl border z-50">
          <div className="bg-orange-600 text-white p-4 rounded-t-lg flex justify-between items-center">
            <h3 className="font-semibold">AI Assistant</h3>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setShowChat(false)}
              className="text-white hover:bg-orange-700"
            >
              ×
            </Button>
          </div>

          <div className="p-4 h-64 overflow-y-auto bg-gray-50">
            <div className="bg-white p-3 rounded-lg mb-3 shadow-sm">
              <p className="text-sm">
                {language === "vi"
                  ? "👋 Xin chào! Tôi là trợ lý AI của hệ thống lab DNU. Tôi có thể giúp bạn:"
                  : "👋 Hello! I'm the DNU lab system AI assistant. I can help you with:"}
              </p>
              <ul className="text-sm mt-2 space-y-1">
                <li>• {language === "vi" ? "Hướng dẫn đặt lịch thiết bị" : "Equipment booking guidance"}</li>
                <li>• {language === "vi" ? "Thông tin về thiết bị" : "Equipment information"}</li>
                <li>• {language === "vi" ? "Giải đáp thắc mắc" : "Answer questions"}</li>
              </ul>
            </div>
          </div>

          <div className="p-4 border-t">
            <div className="flex space-x-2">
              <Input placeholder={currentLang.chatPlaceholder} className="flex-1" />
              <Button size="sm" className="bg-orange-600 hover:bg-orange-700">
                {currentLang.send}
              </Button>
            </div>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid md:grid-cols-3 gap-8">
            <div>
              <div className="flex items-center space-x-3 mb-4">
                <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <BookOpen className="w-5 h-5 text-white" />
                </div>
                <h3 className="text-lg font-semibold">DNU Lab System</h3>
              </div>
              <p className="text-gray-400">
                {language === "vi"
                  ? "Hệ thống quản lý phòng lab hiện đại với công nghệ AI"
                  : "Modern lab management system with AI technology"}
              </p>
            </div>

            <div>
              <h4 className="font-semibold mb-4">{language === "vi" ? "Liên hệ" : "Contact"}</h4>
              <div className="space-y-2 text-gray-400">
                <p>📧 lab@dnu.edu.vn</p>
                <p>📞 +84 236 3653 561</p>
                <p>📍 {language === "vi" ? "Trường Đại học Đại Nam, Hà Nội" : "Dai Nam University, Hanoi"}</p>
              </div>
            </div>

            <div>
              <h4 className="font-semibold mb-4">{language === "vi" ? "Trạng thái hệ thống" : "System Status"}</h4>
              <div className="space-y-2">
                <div className="flex items-center space-x-2">
                  <Badge variant="secondary" className="bg-green-600">
                    {language === "vi" ? "Hoạt động" : "Online"}
                  </Badge>
                  <span className="text-sm text-gray-400">API Server</span>
                </div>
                <div className="flex items-center space-x-2">
                  <Badge variant="secondary" className="bg-green-600">
                    {language === "vi" ? "Hoạt động" : "Online"}
                  </Badge>
                  <span className="text-sm text-gray-400">AI Assistant</span>
                </div>
              </div>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>
              &copy; 2024 DNU Lab Management System.{" "}
              {language === "vi" ? "Tất cả quyền được bảo lưu." : "All rights reserved."}
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default function App() {
  return (
    <AppProvider>
      <HomePage />
    </AppProvider>
  )
}
