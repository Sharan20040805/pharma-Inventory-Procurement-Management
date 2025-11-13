import React from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import InventoryPage from './pages/InventoryPage'
import CopilotChat from './pages/CopilotChat'
import './index.css'

function App(){
  return (
    <BrowserRouter>
      <div className="p-4">
        <nav className="mb-4">
          <Link to="/" className="mr-4 text-blue-600">Inventory</Link>
          <Link to="/copilot" className="text-blue-600">Copilot</Link>
        </nav>
        <Routes>
          <Route path="/" element={<InventoryPage />} />
          <Route path="/copilot" element={<CopilotChat />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}

createRoot(document.getElementById('root')).render(<App />)
