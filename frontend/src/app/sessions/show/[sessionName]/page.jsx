// app/sessions/show/[sessionName]/page.jsx
'use client'

import { useEffect, useState } from 'react'
import { useParams, useSearchParams, useRouter } from 'next/navigation'
import { showSession } from '@/lib/sessions/showSession'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

// Função para formatar o tamanho do arquivo
const formatFileSize = (bytes) => {
  if (!bytes) return '0 B'
  const sizes = ['B', 'KB', 'MB', 'GB']
  const i = Math.floor(Math.log(bytes) / Math.log(1024))
  return Math.round((bytes / Math.pow(1024, i)) * 100) / 100 + ' ' + sizes[i]
}

// Função para formatar a duração
const formatDuration = (seconds) => {
  if (!seconds) return '0s'
  const hours = Math.floor(seconds / 3600)
  const minutes = Math.floor((seconds % 3600) / 60)
  const secs = Math.floor(seconds % 60)

  if (hours > 0) {
    return `${hours}h ${minutes}m ${secs}s`
  } else if (minutes > 0) {
    return `${minutes}m ${secs}s`
  } else {
    return `${secs}s`
  }
}

// Função para formatar a data
const formatDate = (dateString) => {
  if (!dateString) return 'N/A'
  return new Date(dateString).toLocaleString('pt-BR')
}

// Mapeamento de TypeID para emoções (baseado no dataset EmoEEG-MC)
const typeIdToEmotion = {
  19: 'Neutro',
  20: 'Feliz',
  21: 'Triste',
  22: 'Medo',
  23: 'Raiva',
  24: 'Nojo',
}

// Função para obter a cor da emoção
const getEmotionColor = (typeId) => {
  const colorMap = {
    19: 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300',
    20: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
    21: 'bg-blue-100 text-blue-800 dark:bg-blue-900/30 dark:text-blue-300',
    22: 'bg-purple-100 text-purple-800 dark:bg-purple-900/30 dark:text-purple-300',
    23: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
    24: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
  }
  return colorMap[typeId] || 'bg-gray-100 text-gray-800 dark:bg-gray-900/30 dark:text-gray-300'
}

export default function SessionDetail() {
  const params = useParams()
  const searchParams = useSearchParams()
  const router = useRouter()
  const sessionId = searchParams.get('id')
  const sessionName = params.sessionName

  const [session, setSession] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [activeTab, setActiveTab] = useState('overview')

  useEffect(() => {
    if (!sessionId) {
      setError('ID da sessão não encontrado')
      setLoading(false)
      return
    }

    const fetchSession = async () => {
      try {
        setLoading(true)
        setError(null)
        const sessionData = await showSession(sessionId)
        setSession(sessionData)
      } catch (err) {
        console.error('Erro ao carregar sessão:', err)
        setError(err.detail?.[0]?.msg || 'Erro ao carregar detalhes da sessão')
      } finally {
        setLoading(false)
      }
    }

    fetchSession()
  }, [sessionId])

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-6xl mx-auto">
            <div className="flex flex-col items-center justify-center min-h-[60vh]">
              <div className="w-12 h-12 border-4 border-orange-600 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-gray-600 dark:text-gray-400">Carregando detalhes da sessão...</p>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-6xl mx-auto">
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-8 text-center">
              <svg
                className="w-16 h-16 text-red-400 mx-auto mb-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              <h3 className="text-xl font-medium text-red-800 dark:text-red-300 mb-2">
                Erro ao carregar sessão
              </h3>
              <p className="text-red-600 dark:text-red-400 mb-6">{error}</p>
              <div className="flex justify-center gap-4">
                <button
                  onClick={() => window.location.reload()}
                  className="py-2 px-6 bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors duration-200"
                >
                  Tentar Novamente
                </button>
                <Link href="/sessions/list">
                  <button className="py-2 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-colors duration-200">
                    Voltar à Lista
                  </button>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!session) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
        <Navbar />
        <div className="container mx-auto px-4 py-8">
          <div className="max-w-6xl mx-auto">
            <div className="text-center">
              <h1 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                Sessão não encontrada
              </h1>
              <Link href="/sessions/list">
                <button className="py-2 px-6 bg-gradient-to-r from-orange-600 to-orange-700 text-white rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200">
                  Voltar à Lista
                </button>
              </Link>
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-2">
                <Link
                  href="/sessions/list"
                  className="text-orange-600 dark:text-orange-400 hover:text-orange-700 dark:hover:text-orange-300 transition-colors"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M10 19l-7-7m0 0l7-7m-7 7h18"
                    />
                  </svg>
                </Link>
                <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white truncate">
                  {session.session_name}
                </h1>
              </div>
              <p className="text-gray-600 dark:text-gray-400">
                Detalhes completos da sessão de EEG
              </p>
            </div>

            <div className="mt-4 sm:mt-0 flex gap-3">
              <Link href="/sessions/list">
                <button className="py-2 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-700 dark:text-gray-300 font-medium rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 shadow-sm hover:shadow-md flex items-center justify-center gap-2">
                  Voltar à Lista
                </button>
              </Link>
            </div>
          </div>

          {/* Tabs Navigation */}
          <div className="mb-8">
            <div className="flex space-x-1 bg-white dark:bg-[#1e1e1e] rounded-2xl p-2 border border-orange-100 dark:border-orange-900/30 shadow-sm">
              {[
                { id: 'overview', label: 'Visão Geral', icon: '📊' },
                { id: 'annotations', label: 'Anotações', icon: '📝' },
                { id: 'channels', label: 'Canais', icon: '🔌' },
                { id: 'technical', label: 'Técnico', icon: '🔧' },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`flex-1 py-3 px-6 rounded-xl font-medium transition-all duration-300 flex items-center justify-center gap-2 ${
                    activeTab === tab.id
                      ? 'bg-gradient-to-r from-orange-600 to-amber-600 text-white shadow-lg'
                      : 'text-gray-600 dark:text-gray-400 hover:text-orange-600 dark:hover:text-orange-400'
                  }`}
                >
                  <span>{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </div>
          </div>

          {/* Tab Content */}
          <div className="space-y-6">
            {/* Overview Tab */}
            {activeTab === 'overview' && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Informações Principais */}
                <div className="lg:col-span-2 space-y-6">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                      Informações da Sessão
                    </h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          Paciente
                        </label>
                        <p className="text-gray-900 dark:text-white font-medium">
                          {session.patient_iid}
                        </p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          Arquivo
                        </label>
                        <p className="text-gray-900 dark:text-white font-medium truncate">
                          {session.file_name}
                        </p>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          Status
                        </label>
                        <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300">
                          {session.processing_status}
                        </span>
                      </div>
                      <div>
                        <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          Data de Gravação
                        </label>
                        <p className="text-gray-900 dark:text-white font-medium">
                          {formatDate(session.recording_date)}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* Estatísticas Rápidas */}
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-4 border border-orange-100 dark:border-orange-900/30 shadow-sm text-center">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-1">
                        {session.channels}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Canais</div>
                    </div>
                    <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-4 border border-orange-100 dark:border-orange-900/30 shadow-sm text-center">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-1">
                        {session.sample_frequency}Hz
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Frequência</div>
                    </div>
                    <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-4 border border-orange-100 dark:border-orange-900/30 shadow-sm text-center">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-1">
                        {formatDuration(session.duration)}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Duração</div>
                    </div>
                    <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-4 border border-orange-100 dark:border-orange-900/30 shadow-sm text-center">
                      <div className="text-2xl font-bold text-orange-600 dark:text-orange-400 mb-1">
                        {formatFileSize(session.file_size)}
                      </div>
                      <div className="text-sm text-gray-600 dark:text-gray-400">Tamanho</div>
                    </div>
                  </div>
                </div>

                {/* Resumo das Anotações */}
                <div className="space-y-6">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                      Resumo de Emoções
                    </h3>
                    <div className="space-y-3">
                      {Object.entries(typeIdToEmotion).map(([typeId, emotion]) => {
                        const count =
                          session.metadata_json?.annotations?.filter(
                            (annotation) => annotation.description === `TypeID: ${typeId}`,
                          ).length || 0

                        return (
                          <div key={typeId} className="flex justify-between items-center">
                            <span className="text-sm text-gray-600 dark:text-gray-400">
                              {emotion}
                            </span>
                            <span
                              className={`text-xs font-medium px-2 py-1 rounded-full ${getEmotionColor(typeId)}`}
                            >
                              {count}
                            </span>
                          </div>
                        )
                      })}
                    </div>
                  </div>

                  {/* Informações do Sistema */}
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                      Informações do Sistema
                    </h3>
                    <div className="space-y-2 text-sm">
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">ID da Sessão:</span>
                        <span className="text-gray-900 dark:text-white font-mono text-xs">
                          {session.id.substring(0, 8)}...
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">Criada em:</span>
                        <span className="text-gray-900 dark:text-white">
                          {formatDate(session.created_at)}
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-gray-600 dark:text-gray-400">Atualizada em:</span>
                        <span className="text-gray-900 dark:text-white">
                          {formatDate(session.updated_at)}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Annotations Tab */}
            {activeTab === 'annotations' && (
              <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl border border-orange-100 dark:border-orange-900/30 shadow-sm">
                <div className="p-6 border-b border-orange-100 dark:border-orange-900/30">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                    Anotações da Sessão
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400 mt-1">
                    {session.metadata_json?.annotations?.length || 0} eventos registrados
                  </p>
                </div>
                <div className="overflow-x-auto">
                  <table className="w-full">
                    <thead>
                      <tr className="border-b border-orange-100 dark:border-orange-900/30">
                        <th className="text-left p-4 text-sm font-medium text-gray-500 dark:text-gray-400">
                          Tempo
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500 dark:text-gray-400">
                          Emoção
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500 dark:text-gray-400">
                          Tipo
                        </th>
                        <th className="text-left p-4 text-sm font-medium text-gray-500 dark:text-gray-400">
                          Descrição
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      {session.metadata_json?.annotations?.map((annotation, index) => {
                        const typeId = annotation.description.replace('TypeID: ', '')
                        const emotion = typeIdToEmotion[typeId] || 'Desconhecido'

                        return (
                          <tr
                            key={index}
                            className="border-b border-orange-50 dark:border-orange-900/20 hover:bg-orange-50 dark:hover:bg-orange-900/10 transition-colors"
                          >
                            <td className="p-4 text-sm text-gray-900 dark:text-white">
                              {formatDate(annotation.onset)}
                            </td>
                            <td className="p-4">
                              <span
                                className={`text-xs font-medium px-2 py-1 rounded-full ${getEmotionColor(typeId)}`}
                              >
                                {emotion}
                              </span>
                            </td>
                            <td className="p-4 text-sm text-gray-900 dark:text-white">
                              TypeID: {typeId}
                            </td>
                            <td className="p-4 text-sm text-gray-600 dark:text-gray-400">
                              {annotation.duration > 0
                                ? `Duração: ${annotation.duration}s`
                                : 'Evento pontual'}
                            </td>
                          </tr>
                        )
                      })}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Channels Tab */}
            {activeTab === 'channels' && (
              <div className="space-y-6">
                <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Canais EEG
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400 mb-6">
                    {session.metadata_json?.channel_names?.length || 0} canais configurados
                  </p>

                  <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3">
                    {session.metadata_json?.channel_names?.map((channel, index) => (
                      <div
                        key={index}
                        className="bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800/30 rounded-lg p-3 text-center group hover:bg-orange-100 dark:hover:bg-orange-900/30 transition-colors"
                      >
                        <div className="text-lg font-bold text-orange-600 dark:text-orange-400 mb-1">
                          {channel}
                        </div>
                        <div className="text-xs text-gray-600 dark:text-gray-400">
                          Canal {index + 1}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Bad Channels */}
                {session.metadata_json?.bad_channels &&
                  session.metadata_json.bad_channels.length > 0 && (
                    <div className="bg-red-50 dark:bg-red-900/20 rounded-2xl p-6 border border-red-200 dark:border-red-800/30">
                      <h3 className="text-lg font-bold text-red-800 dark:text-red-300 mb-4">
                        ⚠️ Canais com Problemas
                      </h3>
                      <div className="flex flex-wrap gap-2">
                        {session.metadata_json.bad_channels.map((channel, index) => (
                          <span
                            key={index}
                            className="bg-red-100 dark:bg-red-900/30 text-red-800 dark:text-red-300 px-3 py-1 rounded-full text-sm font-medium"
                          >
                            {channel}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
              </div>
            )}

            {/* Technical Tab */}
            {activeTab === 'technical' && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Informações Técnicas
                  </h2>
                  <div className="space-y-4">
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">Caminho do Arquivo</span>
                      <span className="text-gray-900 dark:text-white text-sm font-mono truncate ml-4">
                        {session.file_path}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">Tamanho do Arquivo</span>
                      <span className="text-gray-900 dark:text-white">
                        {formatFileSize(session.file_size)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">Número de Canais</span>
                      <span className="text-gray-900 dark:text-white">{session.channels}</span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">
                        Frequência de Amostragem
                      </span>
                      <span className="text-gray-900 dark:text-white">
                        {session.sample_frequency} Hz
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">Duração Total</span>
                      <span className="text-gray-900 dark:text-white">
                        {formatDuration(session.duration)}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
                      <span className="text-gray-600 dark:text-gray-400">
                        Status de Processamento
                      </span>
                      <span className="text-gray-900 dark:text-white capitalize">
                        {session.processing_status}
                      </span>
                    </div>
                    <div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
  <span className="text-gray-600 dark:text-gray-400">KNN Accuracy</span>
  <span className="text-gray-900 dark:text-white font-mono">0.6342</span>
</div>
<div className="flex justify-between items-center py-2 border-b border-orange-100 dark:border-orange-900/20">
  <span className="text-gray-600 dark:text-gray-400">F1 Score</span>
  <span className="text-gray-900 dark:text-white font-mono">0.6942</span>
</div>
                  </div>
                </div>

                <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Metadados
                  </h2>
                  <div className="space-y-3">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                        ID da Sessão
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400 font-mono bg-orange-50 dark:bg-orange-900/20 p-2 rounded">
                        {session.id}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white mb-2">Criado em</h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {formatDate(session.created_at)}
                      </p>
                    </div>
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white mb-2">
                        Atualizado em
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {formatDate(session.updated_at)}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </main>
    </div>
  )
}
