'use client'

import { useRef, useState } from 'react'

export default function AudioPlayer({ src }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)
  const [volume, setVolume] = useState(1)

  const togglePlayback = () => {
    if (!audioRef.current) return
    if (isPlaying) {
      audioRef.current.pause()
    } else {
      audioRef.current.play().catch((err) => console.log('Erro ao reproduzir:', err))
    }
  }

  const handleVolumeChange = (e) => {
    const vol = parseFloat(e.target.value)
    setVolume(vol)
    if (audioRef.current) {
      audioRef.current.volume = vol
    }
  }

  return (
    <div className="flex flex-col items-center gap-3">
      <audio
        ref={audioRef}
        loop
        onPlay={() => setIsPlaying(true)}
        onPause={() => setIsPlaying(false)}
        onEnded={() => setIsPlaying(false)}
      >
        <source src={src} type="audio/mpeg" />
        Seu navegador não suporta o elemento de áudio.
      </audio>

      {/* Botão Play/Pause */}
      <button
        onClick={togglePlayback}
        className={`w-14 h-14 rounded-full flex items-center justify-center text-2xl transition 
          ${isPlaying ? 'bg-red-500 hover:bg-red-600' : 'bg-green-500 hover:bg-green-600'} 
          text-white shadow-md`}
      >
        {isPlaying ? '⏸️' : '▶️'}
      </button>

      {/* Controle de Volume */}
      <input
        type="range"
        min="0"
        max="1"
        step="0.01"
        value={volume}
        onChange={handleVolumeChange}
        className="w-32 accent-green-500 cursor-pointer"
      />
    </div>
  )
}
