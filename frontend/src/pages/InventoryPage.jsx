import React, { useEffect, useState } from 'react'

export default function InventoryPage(){
  const [medicines, setMedicines] = useState([])

  useEffect(()=>{
    fetch('http://localhost:8000/medicines')
      .then(r=>r.json())
      .then(setMedicines)
  }, [])

  const isExpiring = (expiry_date) => {
    if(!expiry_date) return false
    const d = new Date(expiry_date)
    const now = new Date()
    const diff = (d - now) / (1000*60*60*24)
    return diff < 30
  }

  return (
    <div>
      <h1 className="text-2xl font-bold mb-4">Inventory</h1>
      <table className="min-w-full table-auto">
        <thead>
          <tr>
            <th className="px-2">ID</th>
            <th className="px-2">Name</th>
            <th className="px-2">Qty</th>
            <th className="px-2">Min Stock</th>
            <th className="px-2">Expiry</th>
          </tr>
        </thead>
        <tbody>
          {medicines.map(m=>{
            const low = m.qty < m.min_stock
            const exp = isExpiring(m.expiry_date)
            return (
              <tr key={m.id} className={`${low? 'bg-red-100': ''} ${exp? 'bg-yellow-100': ''}`}>
                <td className="px-2">{m.id}</td>
                <td className="px-2">{m.name}</td>
                <td className="px-2">{m.qty}</td>
                <td className="px-2">{m.min_stock}</td>
                <td className="px-2">{m.expiry_date || '-'}</td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
