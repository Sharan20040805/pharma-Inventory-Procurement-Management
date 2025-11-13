import React, { useState } from 'react'

export default function CopilotChat(){
  const [text, setText] = useState('')
  const [messages, setMessages] = useState([])

  const send = async () => {
    if(!text) return
    setMessages(prev => [...prev, {from:'you', text}])
    setText('')
    const res = await fetch('http://localhost:8000/chat', {
      method: 'POST', headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: text})
    })
    const data = await res.json()
    const reply = data.reply || JSON.stringify(data)
    setMessages(prev => [...prev, {from:'copilot', text: reply}])
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Copilot Chat</h1>
      <div className="mb-4">
        {messages.map((m,i)=> (
          <div key={i} className={`p-2 my-1 ${m.from==='copilot' ? 'bg-gray-100':'bg-blue-50'}`}>
            <strong>{m.from}:</strong> {m.text}
          </div>
        ))}
      </div>
      <div className="flex gap-2">
        <input value={text} onChange={e=>setText(e.target.value)} className="flex-1 p-2 border" />
        <button onClick={send} className="px-4 py-2 bg-blue-600 text-white">Send</button>
      </div>
      <div className="text-sm text-gray-600 mt-2">Try: "low stock" or "predict paracetamol"</div>
    </div>
  )
}
