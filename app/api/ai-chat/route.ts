import { type NextRequest, NextResponse } from "next/server"

export async function POST(request: NextRequest) {
  try {
    const { message, language, context } = await request.json()

    // Tích hợp với Gemini AI (bạn cần API key)
    const response = await fetch(
      "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=YOUR_GEMINI_API_KEY",
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          contents: [
            {
              parts: [
                {
                  text: `You are a smart AI assistant for a lab management system. Context: ${context}. Language: ${language}. User question: ${message}. Please provide helpful and accurate responses about lab equipment, booking procedures, and system usage.`,
                },
              ],
            },
          ],
        }),
      },
    )

    const data = await response.json()
    const aiResponse =
      data.candidates?.[0]?.content?.parts?.[0]?.text ||
      (language === "vi" ? "Xin lỗi, tôi không thể trả lời câu hỏi này." : "Sorry, I cannot answer this question.")

    return NextResponse.json({ response: aiResponse })
  } catch (error) {
    console.error("AI API Error:", error)
    return NextResponse.json({ error: "AI service unavailable" }, { status: 500 })
  }
}
