// app/scientist/profile/page.jsx
'use client'

import { useEffect, useState } from 'react'
import { useAuth } from '@/hooks/useAuth'
import { fetchProfile } from '@/lib/fetchProfile'
import { updateScientist } from '@/lib/updateScientist'
import Navbar from '@/components/ui/Navbar'
import Link from 'next/link'

// Função para formatar o gênero
const formatGender = (gender) => {
  const genderMap = {
    male: 'Masculino',
    female: 'Feminino',
    other: 'Outro',
    unknown: 'Não informado',
  }
  return genderMap[gender] || 'Não informado'
}

export default function ScientistProfile() {
  const { user, requireAuth, isLoading } = useAuth()
  const [profile, setProfile] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [isEditing, setIsEditing] = useState(false)
  const [editLoading, setEditLoading] = useState(false)
  const [editError, setEditError] = useState(null)
  const [editSuccess, setEditSuccess] = useState(false)
  const [selectedFile, setSelectedFile] = useState(null)
  const [imagePreview, setImagePreview] = useState(null)

  // Dados do formulário de edição
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    institution: '',
    specialization: '',
    gender: '',
    age: '',
  })

  useEffect(() => {
    requireAuth('/scientist/login')
  }, [requireAuth])

  // Carregar perfil do cientista
  useEffect(() => {
    if (!user) return

    const loadProfile = async () => {
      try {
        setLoading(true)
        setError(null)
        const profileData = await fetchProfile()
        setProfile(profileData)
        // Preencher formulário com dados atuais
        setFormData({
          first_name: profileData.first_name || '',
          last_name: profileData.last_name || '',
          institution: profileData.institution || '',
          specialization: profileData.specialization || '',
          gender: profileData.gender || '',
          age: profileData.age || '',
        })
        // Set image preview if profile picture exists
        if (profileData.profilePicture) {
          setImagePreview(profileData.profilePicture)
        }
      } catch (err) {
        setError(err.message)
        console.error('Erro ao carregar perfil:', err)
      } finally {
        setLoading(false)
      }
    }

    loadProfile()
  }, [user])

  const handleEdit = () => {
    setIsEditing(true)
    setEditError(null)
    setEditSuccess(false)
  }

  const handleCancel = () => {
    setIsEditing(false)
    // Restaurar dados originais
    setFormData({
      first_name: profile.first_name || '',
      last_name: profile.last_name || '',
      institution: profile.institution || '',
      specialization: profile.specialization || '',
      gender: profile.gender || '',
      age: profile.age || '',
    })
    setSelectedFile(null)
    setImagePreview(profile.profilePicture || null)
    setEditError(null)
  }

  const handleFileSelect = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validar tipo de arquivo
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif', 'image/webp']
      if (!validTypes.includes(file.type)) {
        setEditError('Por favor, selecione uma imagem válida (JPEG, PNG, GIF, WebP)')
        return
      }

      // Validar tamanho do arquivo (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setEditError('A imagem deve ter no máximo 5MB')
        return
      }

      setSelectedFile(file)

      // Criar preview da imagem
      const reader = new FileReader()
      reader.onloadend = () => {
        setImagePreview(reader.result)
      }
      reader.readAsDataURL(file)
      setEditError(null)
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setEditLoading(true)
    setEditError(null)
    setEditSuccess(false)

    try {
      const submitData = { ...formData }

      // Se há um arquivo selecionado, adicionar ao FormData
      if (selectedFile) {
        submitData.profilePicture = selectedFile
      }

      const result = await updateScientist(submitData)

      // Atualizar o perfil com os novos dados
      const updatedProfile = {
        ...profile,
        ...formData,
        profilePicture: imagePreview, // Usar a preview temporária até recarregar o perfil
      }

      setProfile(updatedProfile)
      setEditSuccess(true)
      setIsEditing(false)
      setSelectedFile(null)

      // Limpar mensagem de sucesso após 3 segundos
      setTimeout(() => setEditSuccess(false), 3000)
    } catch (err) {
      setEditError(err.message)
      console.error('Erro ao atualizar perfil:', err)
    } finally {
      setEditLoading(false)
    }
  }

  const handleChange = (e) => {
    const { name, value } = e.target
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }))
  }

  if (isLoading || loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f] flex items-center justify-center">
        <div className="flex flex-col items-center">
          <div className="w-12 h-12 border-4 border-orange-600 border-t-transparent rounded-full animate-spin mb-4"></div>
          <p className="text-gray-600 dark:text-gray-400">Carregando perfil...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
      <Navbar />

      <main className="container mx-auto px-4 py-8">
        <div className="max-w-4xl mx-auto">
          {/* Header */}
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
            <div>
              <h1 className="text-3xl lg:text-4xl font-bold text-gray-900 dark:text-white mb-2">
                Meu Perfil
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Gerencie suas informações pessoais e profissionais
              </p>
            </div>

            <Link href="/dashboard" className="mt-4 sm:mt-0">
              <button className="py-2 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-900 dark:text-white font-medium rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 shadow-sm hover:shadow-md flex items-center justify-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M10 19l-7-7m0 0l7-7m-7 7h18"
                  />
                </svg>
                Voltar ao Dashboard
              </button>
            </Link>
          </div>

          {/* Error State */}
          {error && (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-6 mb-6">
              <div className="flex items-center gap-3">
                <svg
                  className="w-5 h-5 text-red-400"
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
                <div>
                  <h3 className="text-lg font-medium text-red-800 dark:text-red-300 mb-1">
                    Erro ao carregar perfil
                  </h3>
                  <p className="text-red-600 dark:text-red-400">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Success Message */}
          {editSuccess && (
            <div className="bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded-lg p-6 mb-6">
              <div className="flex items-center gap-3">
                <svg
                  className="w-5 h-5 text-green-400"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
                  />
                </svg>
                <div>
                  <h3 className="text-lg font-medium text-green-800 dark:text-green-300 mb-1">
                    Perfil atualizado com sucesso!
                  </h3>
                  <p className="text-green-600 dark:text-green-400">
                    Suas informações foram salvas.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* Profile Card */}
          {profile && (
            <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl shadow-xl border border-orange-100 dark:border-orange-900/30 overflow-hidden">
              {/* Header do Card */}
              <div className="bg-gradient-to-r from-orange-50 to-amber-50 dark:from-orange-900/20 dark:to-amber-900/20 p-6 border-b border-orange-100 dark:border-orange-900/30">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="relative">
                      <div className="w-16 h-16 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center border-2 border-orange-200 dark:border-orange-800/30 overflow-hidden">
                        {imagePreview ? (
                          <img
                            src={imagePreview}
                            alt="Foto de perfil"
                            className="w-full h-full rounded-full object-cover"
                          />
                        ) : (
                          <span className="text-2xl text-orange-600 dark:text-orange-400 font-medium">
                            {profile.first_name?.[0]}
                            {profile.last_name?.[0]}
                          </span>
                        )}
                      </div>
                      {isEditing && (
                        <label className="absolute -bottom-1 -right-1 bg-orange-600 text-white p-1 rounded-full cursor-pointer hover:bg-orange-700 transition-colors duration-200">
                          <svg
                            className="w-4 h-4"
                            fill="none"
                            stroke="currentColor"
                            viewBox="0 0 24 24"
                          >
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z"
                            />
                            <path
                              strokeLinecap="round"
                              strokeLinejoin="round"
                              strokeWidth={2}
                              d="M15 13a3 3 0 11-6 0 3 3 0 016 0z"
                            />
                          </svg>
                          <input
                            type="file"
                            className="hidden"
                            accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                            onChange={handleFileSelect}
                          />
                        </label>
                      )}
                    </div>
                    <div>
                      <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                        {profile.first_name} {profile.last_name}
                      </h2>
                      <p className="text-gray-600 dark:text-gray-400">{profile.email}</p>
                    </div>
                  </div>

                  {!isEditing && (
                    <button
                      onClick={handleEdit}
                      className="py-2 px-4 bg-gradient-to-r from-orange-600 to-orange-700 text-white font-medium rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200 shadow-md hover:shadow-lg flex items-center justify-center gap-2"
                    >
                      <svg
                        className="w-4 h-4"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                      </svg>
                      Editar Perfil
                    </button>
                  )}
                </div>
              </div>

              {/* Formulário/Informações */}
              <div className="p-6">
                {isEditing ? (
                  <form onSubmit={handleSubmit} className="space-y-6">
                    {/* Edit Error */}
                    {editError && (
                      <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4">
                        <p className="text-red-600 dark:text-red-400 text-sm">{editError}</p>
                      </div>
                    )}

                    {/* Upload de Foto - Versão Desktop */}
                    <div className="hidden md:block">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Foto de Perfil
                      </label>
                      <div className="flex items-center gap-6">
                        <div className="relative">
                          <div className="w-24 h-24 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center border-2 border-orange-200 dark:border-orange-800/30 overflow-hidden">
                            {imagePreview ? (
                              <img
                                src={imagePreview}
                                alt="Preview da foto"
                                className="w-full h-full rounded-full object-cover"
                              />
                            ) : (
                              <span className="text-3xl text-orange-600 dark:text-orange-400 font-medium">
                                {profile.first_name?.[0]}
                                {profile.last_name?.[0]}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="flex-1">
                          <div className="flex gap-3">
                            <label className="flex-1 py-2 px-4 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 text-center cursor-pointer font-medium">
                              Escolher Arquivo
                              <input
                                type="file"
                                className="hidden"
                                accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                                onChange={handleFileSelect}
                              />
                            </label>
                            <button
                              type="button"
                              onClick={() => {
                                setSelectedFile(null)
                                setImagePreview(profile.profilePicture || null)
                              }}
                              className="py-2 px-4 bg-white dark:bg-[#2a2a2a] border border-red-200 dark:border-red-800/50 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200 font-medium"
                            >
                              Remover
                            </button>
                          </div>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-2">
                            PNG, JPG, GIF ou WebP. Máx. 5MB.
                          </p>
                        </div>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Nome
                        </label>
                        <input
                          type="text"
                          name="first_name"
                          value={formData.first_name}
                          onChange={handleChange}
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Sobrenome
                        </label>
                        <input
                          type="text"
                          name="last_name"
                          value={formData.last_name}
                          onChange={handleChange}
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Instituição
                        </label>
                        <input
                          type="text"
                          name="institution"
                          value={formData.institution}
                          onChange={handleChange}
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Especialização
                        </label>
                        <input
                          type="text"
                          name="specialization"
                          value={formData.specialization}
                          onChange={handleChange}
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        />
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Gênero
                        </label>
                        <select
                          name="gender"
                          value={formData.gender}
                          onChange={handleChange}
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        >
                          <option value="">Selecione o gênero</option>
                          <option value="male">Masculino</option>
                          <option value="female">Feminino</option>
                          <option value="other">Outro</option>
                          <option value="unknown">Prefiro não informar</option>
                        </select>
                      </div>

                      <div>
                        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                          Idade
                        </label>
                        <input
                          type="number"
                          name="age"
                          value={formData.age}
                          onChange={handleChange}
                          min="18"
                          max="100"
                          className="w-full px-3 py-2 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-orange-300 dark:focus:border-orange-600 transition-all duration-200 text-gray-900 dark:text-white"
                        />
                      </div>
                    </div>

                    {/* Upload de Foto - Versão Mobile */}
                    <div className="md:hidden">
                      <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-3">
                        Foto de Perfil
                      </label>
                      <div className="flex flex-col gap-4">
                        <div className="flex justify-center">
                          <div className="relative">
                            <div className="w-20 h-20 bg-gradient-to-br from-orange-100 to-amber-100 dark:from-orange-900/30 dark:to-amber-900/30 rounded-full flex items-center justify-center border-2 border-orange-200 dark:border-orange-800/30 overflow-hidden">
                              {imagePreview ? (
                                <img
                                  src={imagePreview}
                                  alt="Preview da foto"
                                  className="w-full h-full rounded-full object-cover"
                                />
                              ) : (
                                <span className="text-2xl text-orange-600 dark:text-orange-400 font-medium">
                                  {profile.first_name?.[0]}
                                  {profile.last_name?.[0]}
                                </span>
                              )}
                            </div>
                          </div>
                        </div>
                        <div className="flex gap-3">
                          <label className="flex-1 py-2 px-4 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 text-center cursor-pointer font-medium">
                            Escolher Arquivo
                            <input
                              type="file"
                              className="hidden"
                              accept="image/jpeg,image/jpg,image/png,image/gif,image/webp"
                              onChange={handleFileSelect}
                            />
                          </label>
                          <button
                            type="button"
                            onClick={() => {
                              setSelectedFile(null)
                              setImagePreview(profile.profilePicture || null)
                            }}
                            className="py-2 px-4 bg-white dark:bg-[#2a2a2a] border border-red-200 dark:border-red-800/50 text-red-600 dark:text-red-400 rounded-lg hover:bg-red-50 dark:hover:bg-red-900/20 transition-all duration-200 font-medium"
                          >
                            Remover
                          </button>
                        </div>
                        <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
                          PNG, JPG, GIF ou WebP. Máx. 5MB.
                        </p>
                      </div>
                    </div>

                    {/* Botões de ação */}
                    <div className="flex gap-3 pt-4 border-t border-orange-100 dark:border-orange-900/30">
                      <button
                        type="button"
                        onClick={handleCancel}
                        className="flex-1 py-3 px-4 bg-white dark:bg-[#2a2a2a] border border-orange-200 dark:border-orange-800/50 text-gray-800 dark:text-gray-200 rounded-lg hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-200 text-center font-medium"
                      >
                        Cancelar
                      </button>
                      <button
                        type="submit"
                        disabled={editLoading}
                        className="flex-1 py-3 px-4 bg-gradient-to-r from-orange-600 to-orange-700 text-white font-medium rounded-lg hover:from-orange-700 hover:to-orange-800 transition-all duration-200 shadow-md hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        {editLoading ? 'Salvando...' : 'Salvar Alterações'}
                      </button>
                    </div>
                  </form>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Nome
                      </label>
                      <p className="text-gray-900 dark:text-white">{profile.first_name}</p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Sobrenome
                      </label>
                      <p className="text-gray-900 dark:text-white">{profile.last_name}</p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Email
                      </label>
                      <p className="text-gray-900 dark:text-white">{profile.email}</p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Instituição
                      </label>
                      <p className="text-gray-900 dark:text-white">
                        {profile.institution || 'Não informado'}
                      </p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Especialização
                      </label>
                      <p className="text-gray-900 dark:text-white">
                        {profile.specialization || 'Não informado'}
                      </p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Gênero
                      </label>
                      <p className="text-gray-900 dark:text-white">
                        {formatGender(profile.gender)}
                      </p>
                    </div>

                    <div className="space-y-1">
                      <label className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        Idade
                      </label>
                      <p className="text-gray-900 dark:text-white">
                        {profile.age ? `${profile.age} anos` : 'Não informado'}
                      </p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
