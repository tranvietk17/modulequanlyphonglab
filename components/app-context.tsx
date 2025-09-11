"use client"

import { createContext, useContext, useState, useEffect, type ReactNode } from "react"

interface User {
  id: number
  name: string
  email: string
  role: "student" | "admin" | "teacher"
  department: string
  status: "active" | "inactive"
  studentId?: string
}

interface Booking {
  id: number
  equipment: string
  department: string
  room: string
  date: string
  pickupTime: string
  returnTime: string
  status: "pending" | "approved" | "rejected"
  studentName: string
  studentEmail: string
  purpose: string
}

interface Equipment {
  id: number
  name: string
  department: string
  room: string
  status: "available" | "in-use" | "maintenance"
  description: string
  quantity: number
  available: number
}

interface AppContextType {
  users: User[]
  bookings: Booking[]
  equipment: Equipment[]
  addUser: (user: Omit<User, "id">) => void
  addBooking: (booking: Omit<Booking, "id">) => void
  updateBooking: (id: number, updates: Partial<Booking>) => void
  updateUser: (id: number, updates: Partial<User>) => void
  updateEquipment: (id: number, updates: Partial<Equipment>) => void
  getUserByEmail: (email: string) => User | undefined
}

const AppContext = createContext<AppContextType | undefined>(undefined)

export { AppContext }

export function AppProvider({ children }: { children: ReactNode }) {
  const [users, setUsers] = useState<User[]>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("lab-users")
      if (saved) return JSON.parse(saved)
    }
    return [
      {
        id: 1,
        name: "Nguyễn Văn A",
        email: "student@dnu.edu.vn",
        role: "student",
        department: "Khoa Sinh học",
        status: "active",
        studentId: "2024001234",
      },
      {
        id: 2,
        name: "Trần Thị B",
        email: "admin@dnu.edu.vn",
        role: "admin",
        department: "Quản trị",
        status: "active",
      },
      {
        id: 3,
        name: "Lê Văn C",
        email: "student2@dnu.edu.vn",
        role: "student",
        department: "Khoa Vật lý",
        status: "active",
        studentId: "2024001235",
      },
      {
        id: 4,
        name: "Phạm Thị D",
        email: "student3@dnu.edu.vn",
        role: "student",
        department: "Khoa Hóa học",
        status: "active",
        studentId: "2024001236",
      },
      {
        id: 5,
        name: "Hoàng Văn E",
        email: "student4@dnu.edu.vn",
        role: "student",
        department: "Khoa Công nghệ thông tin",
        status: "active",
        studentId: "2024001237",
      },
    ]
  })

  const [bookings, setBookings] = useState<Booking[]>(() => {
    if (typeof window !== "undefined") {
      const saved = localStorage.getItem("lab-bookings")
      if (saved) return JSON.parse(saved)
    }
    return [
      {
        id: 1,
        equipment: "Máy ly tâm Centrifuge CF-15",
        department: "Khoa Sinh học",
        room: "Lab B101",
        date: "2024-01-15",
        pickupTime: "14:00",
        returnTime: "16:00",
        status: "approved",
        studentName: "Nguyễn Văn A",
        studentEmail: "student@dnu.edu.vn",
        purpose: "Thí nghiệm tách protein",
      },
      {
        id: 2,
        equipment: "Kính hiển vi điện tử SEM-2000",
        department: "Khoa Vật lý",
        room: "Lab P205",
        date: "2024-01-16",
        pickupTime: "09:00",
        returnTime: "11:00",
        status: "pending",
        studentName: "Lê Văn C",
        studentEmail: "student2@dnu.edu.vn",
        purpose: "Quan sát cấu trúc vật liệu nano",
      },
    ]
  })

  const [equipment, setEquipment] = useState<Equipment[]>(() => {
    if (typeof window !== "undefined") {
      localStorage.removeItem("lab-equipment")
    }
    return [
      // Khoa Sinh học - 3 thiết bị
      {
        id: 1,
        name: "Máy ly tâm Centrifuge CF-15",
        department: "Khoa Sinh học",
        room: "Lab B101",
        status: "available",
        description: "Máy ly tâm tốc độ cao cho tách protein và DNA",
        quantity: 2,
        available: 2,
      },
      {
        id: 2,
        name: "Máy PCR Thermal Cycler",
        department: "Khoa Sinh học",
        room: "Lab B102",
        status: "available",
        description: "Máy khuếch đại DNA bằng phản ứng chuỗi polymerase",
        quantity: 1,
        available: 1,
      },
      {
        id: 3,
        name: "Tủ ấm CO2 Incubator",
        department: "Khoa Sinh học",
        room: "Lab B103",
        status: "available",
        description: "Tủ ấm nuôi cấy tế bào với môi trường CO2",
        quantity: 1,
        available: 1,
      },
      // Khoa Vật lý - 3 thiết bị
      {
        id: 4,
        name: "Kính hiển vi điện tử SEM-2000",
        department: "Khoa Vật lý",
        room: "Lab P205",
        status: "available",
        description: "Kính hiển vi điện tử quét độ phân giải cao",
        quantity: 1,
        available: 1,
      },
      {
        id: 5,
        name: "Máy đo tính chất vật liệu UTM",
        department: "Khoa Vật lý",
        room: "Lab P206",
        status: "available",
        description: "Máy kiểm tra độ bền kéo và nén vật liệu",
        quantity: 2,
        available: 2,
      },
      {
        id: 6,
        name: "Máy quang phổ Raman",
        department: "Khoa Vật lý",
        room: "Lab P207",
        status: "available",
        description: "Máy phân tích cấu trúc phân tử bằng tán xạ Raman",
        quantity: 1,
        available: 1,
      },
      // Khoa Hóa học - 3 thiết bị
      {
        id: 7,
        name: "Máy quang phổ UV-Vis",
        department: "Khoa Hóa học",
        room: "Lab C301",
        status: "available",
        description: "Máy đo quang phổ tử ngoại-khả kiến",
        quantity: 2,
        available: 2,
      },
      {
        id: 8,
        name: "Máy sắc ký khí GC-MS",
        department: "Khoa Hóa học",
        room: "Lab C302",
        status: "available",
        description: "Máy sắc ký khí kết hợp khối phổ",
        quantity: 1,
        available: 1,
      },
      {
        id: 9,
        name: "Máy chuẩn độ tự động",
        department: "Khoa Hóa học",
        room: "Lab C303",
        status: "available",
        description: "Máy chuẩn độ acid-base tự động",
        quantity: 2,
        available: 2,
      },
      // Khoa Công nghệ thông tin - 3 thiết bị
      {
        id: 10,
        name: "Máy chủ GPU Tesla V100",
        department: "Khoa Công nghệ thông tin",
        room: "Lab IT401",
        status: "available",
        description: "Máy chủ GPU cho machine learning và AI",
        quantity: 1,
        available: 1,
      },
      {
        id: 11,
        name: "Thiết bị mạng Cisco Router",
        department: "Khoa Công nghệ thông tin",
        room: "Lab IT402",
        status: "available",
        description: "Router chuyên nghiệp cho thực hành mạng",
        quantity: 2,
        available: 2,
      },
      {
        id: 12,
        name: "Máy in 3D Ultimaker",
        department: "Khoa Công nghệ thông tin",
        room: "Lab IT403",
        status: "available",
        description: "Máy in 3D độ chính xác cao",
        quantity: 1,
        available: 1,
      },
    ]
  })

  useEffect(() => {
    localStorage.setItem("lab-users", JSON.stringify(users))
  }, [users])

  useEffect(() => {
    localStorage.setItem("lab-bookings", JSON.stringify(bookings))
  }, [bookings])

  useEffect(() => {
    localStorage.setItem("lab-equipment", JSON.stringify(equipment))
  }, [equipment])

  const addUser = (userData: Omit<User, "id">) => {
    const newUser = {
      ...userData,
      id: Math.max(...users.map((u) => u.id), 0) + 1,
    }
    setUsers((prev) => [...prev, newUser])
  }

  const addBooking = (bookingData: Omit<Booking, "id">) => {
    const newBooking = {
      ...bookingData,
      id: Math.max(...bookings.map((b) => b.id), 0) + 1,
    }
    setBookings((prev) => [...prev, newBooking])
  }

  const updateBooking = (id: number, updates: Partial<Booking>) => {
    setBookings((prev) => prev.map((booking) => (booking.id === id ? { ...booking, ...updates } : booking)))
  }

  const updateUser = (id: number, updates: Partial<User>) => {
    setUsers((prev) => prev.map((user) => (user.id === id ? { ...user, ...updates } : user)))
  }

  const updateEquipment = (id: number, updates: Partial<Equipment>) => {
    setEquipment((prev) => prev.map((eq) => (eq.id === id ? { ...eq, ...updates } : eq)))
  }

  const getUserByEmail = (email: string) => {
    return users.find((user) => user.email === email)
  }

  return (
    <AppContext.Provider
      value={{
        users,
        bookings,
        equipment,
        addUser,
        addBooking,
        updateBooking,
        updateUser,
        updateEquipment,
        getUserByEmail,
      }}
    >
      {children}
    </AppContext.Provider>
  )
}

export function useAppContext() {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error("useAppContext must be used within an AppProvider")
  }
  return context
}
