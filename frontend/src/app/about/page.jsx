'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'

export default function About() {
  const [activeSection, setActiveSection] = useState('overview')

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-amber-50 dark:from-[#0f0f0f] dark:via-[#1a1a1a] dark:to-[#0f0f0f]">
      {/* Header */}
      <header className="border-b border-orange-100 dark:border-orange-900/30 bg-white/80 dark:bg-[#1e1e1e]/80 backdrop-blur-sm sticky top-0 z-10">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <Link href="/" className="flex items-center space-x-2 group">
              <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-amber-500 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
                <span className="text-white font-bold text-lg">M</span>
              </div>
              <span className="text-2xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent">
                MANGO
              </span>
            </Link>

            <nav className="hidden md:flex items-center space-x-8">
              {['overview', 'technology', 'applications', 'team'].map((section) => (
                <button
                  key={section}
                  onClick={() => setActiveSection(section)}
                  className={`font-medium transition-all duration-200 ${
                    activeSection === section
                      ? 'text-orange-600 dark:text-orange-400'
                      : 'text-gray-600 dark:text-gray-400 hover:text-orange-500 dark:hover:text-orange-300'
                  }`}
                >
                  {section === 'overview' && 'Visão Geral'}
                  {section === 'technology' && 'Tecnologia'}
                  {section === 'applications' && 'Aplicações'}
                  {section === 'team' && 'Equipe'}
                </button>
              ))}
            </nav>

            <Link href="/">
              <button className="py-2 px-6 bg-white dark:bg-[#1e1e1e] border border-orange-200 dark:border-orange-800/50 text-gray-700 dark:text-gray-300 font-medium rounded-xl hover:bg-orange-50 dark:hover:bg-orange-900/20 transition-all duration-300 hover:-translate-y-0.5">
                Voltar ao Início
              </button>
            </Link>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-12">
        {/* Hero Section */}
        <div className="text-center max-w-4xl mx-auto mb-16">
          <h1 className="text-5xl lg:text-7xl font-bold bg-gradient-to-r from-orange-600 to-amber-600 bg-clip-text text-transparent mb-6">
            MANGO
          </h1>
          <p className="text-xl lg:text-2xl text-gray-600 dark:text-gray-300 font-light mb-8 leading-relaxed">
            Mindwave Analysis for Neurofeedback & Graphical Observation
          </p>
          <p className="text-lg text-gray-600 dark:text-gray-400 max-w-3xl mx-auto leading-relaxed">
            Conectando dados de EEG a representações visuais interativas em 3D para revolucionar a
            compreensão das respostas cerebrais humanas.
          </p>
        </div>

        {/* Mobile Navigation */}
        <div className="md:hidden mb-8">
          <div className="flex overflow-x-auto space-x-2 pb-2">
            {['overview', 'technology', 'applications', 'team'].map((section) => (
              <button
                key={section}
                onClick={() => setActiveSection(section)}
                className={`flex-shrink-0 px-4 py-2 rounded-full text-sm font-medium transition-all duration-200 ${
                  activeSection === section
                    ? 'bg-orange-600 text-white shadow-lg'
                    : 'bg-white dark:bg-[#1e1e1e] text-gray-600 dark:text-gray-400 border border-orange-100 dark:border-orange-800/30'
                }`}
              >
                {section === 'overview' && 'Visão Geral'}
                {section === 'technology' && 'Tecnologia'}
                {section === 'applications' && 'Aplicações'}
                {section === 'team' && 'Equipe'}
              </button>
            ))}
          </div>
        </div>

        {/* Content Sections */}
        <div className="max-w-6xl mx-auto">
          {/* Overview Section */}
          {activeSection === 'overview' && (
            <div className="space-y-12">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
                <div className="space-y-8">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-8 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                      Sobre o Projeto
                    </h2>
                    <div className="space-y-4 text-gray-600 dark:text-gray-300 leading-relaxed">
                      <p>
                        O <strong>MANGO</strong> é uma interface cérebro-computador inovadora que
                        utiliza a base de dados <strong>EmoEEG-MC</strong> para reproduzir em
                        modelos 3D as áreas do cérebro estimuladas por diferentes contextos
                        emocionais.
                      </p>
                      <p>
                        Desenvolvido como projeto integrador do curso de Ciência da Computação da
                        UTFPR, nosso objetivo é criar uma ponte entre dados complexos de EEG e
                        representações visuais intuitivas e interativas.
                      </p>
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-orange-50 to-amber-50 dark:from-orange-900/10 dark:to-amber-900/10 rounded-2xl p-8 border border-orange-200 dark:border-orange-800/30">
                    <div className="text-center">
                      <div className="w-16 h-16 bg-orange-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg
                          className="w-8 h-8 text-white"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M13 10V3L4 14h7v7l9-11h-7z"
                          />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                        Arquitetura do Sistema
                      </h3>
                      <div className="relative h-82 bg-white dark:bg-[#1e1e1e] rounded-xl border border-orange-100 dark:border-orange-800/30 flex items-center justify-center">
                        <Image
                          src="/images/imagem1.png"
                          alt="Arquitetura do Sistema MANGO"
                          fill
                          className="object-contain rounded-xl"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                <div className="space-y-8">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-8 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                      Objetivos Principais
                    </h3>
                    <div className="space-y-4">
                      {[
                        {
                          icon: '🧠',
                          title: 'Análise de EEG',
                          description:
                            'Processar sinais cerebrais para identificar padrões emocionais',
                        },
                        {
                          icon: '📊',
                          title: 'Visualização 3D',
                          description:
                            'Representar áreas cerebrais ativadas em modelos interativos',
                        },
                        {
                          icon: '🔬',
                          title: 'Pesquisa Científica',
                          description: 'Contribuir para estudos em neurociência e psicologia',
                        },
                        {
                          icon: '🎯',
                          title: 'Aplicações Práticas',
                          description: 'Oferecer ferramentas para marketing, saúde e educação',
                        },
                      ].map((item, index) => (
                        <div
                          key={index}
                          className="flex items-start space-x-4 p-4 rounded-lg bg-orange-50 dark:bg-orange-900/10 border border-orange-100 dark:border-orange-800/30"
                        >
                          <span className="text-2xl flex-shrink-0">{item.icon}</span>
                          <div>
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                              {item.title}
                            </h4>
                            <p className="text-gray-600 dark:text-gray-300 text-sm mt-1">
                              {item.description}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="bg-gradient-to-br from-amber-50 to-orange-50 dark:from-amber-900/10 dark:to-orange-900/10 rounded-2xl p-8 border border-amber-200 dark:border-amber-800/30">
                    <div className="text-center">
                      <div className="w-16 h-16 bg-amber-500 rounded-full flex items-center justify-center mx-auto mb-4">
                        <svg
                          className="w-8 h-8 text-white"
                          fill="none"
                          stroke="currentColor"
                          viewBox="0 0 24 24"
                        >
                          <path
                            strokeLinecap="round"
                            strokeLinejoin="round"
                            strokeWidth={2}
                            d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"
                          />
                        </svg>
                      </div>
                      <h3 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
                        Visualização de ondas cerebrais
                      </h3>
                      <div className="relative h-60 bg-white dark:bg-[#1e1e1e] rounded-xl border border-amber-100 dark:border-amber-800/30 flex items-center justify-center">
                        <Image
                          src="/images/imagem2.png"
                          alt="Interface do Sistema MANGO"
                          fill
                          className="object-contain rounded-xl"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Technology Section */}
          {activeSection === 'technology' && (
            <div className="space-y-12">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
                <div className="space-y-8">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-8 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">
                      Base de Dados EmoEEG-MC
                    </h2>
                    <div className="space-y-4 text-gray-600 dark:text-gray-300 leading-relaxed">
                      <p>
                        Utilizamos a{' '}
                        <strong>
                          EmoEEG-MC: A Multi-Context Emotional EEG Dataset for Cross-Context Emotion
                          Decoding
                        </strong>
                        , uma base de dados abrangente que permite a decodificação emocional entre
                        diferentes contextos.
                      </p>
                      <p>
                        Esta base fornece dados de EEG de alta qualidade capturados em múltiplos
                        contextos emocionais, permitindo treinar modelos robustos de machine
                        learning para reconhecimento de padrões emocionais.
                      </p>
                    </div>
                  </div>

                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-8 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                      Tecnologias Utilizadas
                    </h3>
                    <div className="grid grid-cols-2 gap-4">
                      {[
                        { name: 'Next.js', color: 'from-gray-600 to-gray-800' },
                        { name: 'React Three', color: 'from-purple-500 to-purple-700' },
                        { name: 'Django', color: 'from-blue-500 to-blue-700' },
                        { name: 'FastAPI', color: 'from-orange-500 to-orange-700' },
                        { name: 'EEG Analysis', color: 'from-green-500 to-green-700' },
                      ].map((tech, index) => (
                        <div key={index} className="text-center">
                          <div
                            className={`w-12 h-12 bg-gradient-to-br ${tech.color} rounded-lg flex items-center justify-center mx-auto mb-2`}
                          >
                            <span className="text-white font-bold text-xs">
                              {tech.name.split(' ')[0]}
                            </span>
                          </div>
                          <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                            {tech.name}
                          </span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

                <div className="space-y-8">
                  <div className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-8 border border-orange-100 dark:border-orange-900/30 shadow-sm">
                    <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-6">
                      Fluxo de Processamento
                    </h3>
                    <div className="space-y-6">
                      {[
                        {
                          step: '1',
                          title: 'Captura de EEG',
                          description: 'Coleta de sinais cerebrais brutos',
                        },
                        {
                          step: '2',
                          title: 'Pré-processamento',
                          description: 'Filtragem e limpeza dos dados',
                        },
                        {
                          step: '3',
                          title: 'Análise de Features',
                          description: 'Extração de características relevantes',
                        },
                        {
                          step: '4',
                          title: 'Classificação',
                          description: 'Identificação de padrões emocionais',
                        },
                        {
                          step: '5',
                          title: 'Visualização 3D',
                          description: 'Mapeamento para modelo interativo',
                        },
                      ].map((item, index) => (
                        <div key={index} className="flex items-center space-x-4">
                          <div className="w-8 h-8 bg-gradient-to-br from-orange-500 to-amber-500 rounded-full flex items-center justify-center flex-shrink-0">
                            <span className="text-white font-bold text-sm">{item.step}</span>
                          </div>
                          <div className="flex-1">
                            <h4 className="font-semibold text-gray-900 dark:text-white">
                              {item.title}
                            </h4>
                            <p className="text-gray-600 dark:text-gray-300 text-sm">
                              {item.description}
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Applications Section */}
          {activeSection === 'applications' && (
            <div className="space-y-12">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
                {[
                  {
                    icon: '🔬',
                    title: 'Pesquisa Científica',
                    description:
                      'Análise das respostas neurais em estudos de neurociência para compreensão dos mecanismos emocionais.',
                    color: 'from-blue-500 to-blue-600',
                  },
                  {
                    icon: '📈',
                    title: 'Neuromarketing',
                    description:
                      'Avaliação de estímulos emocionais de consumidores a campanhas, produtos e contextos comerciais.',
                    color: 'from-green-500 to-green-600',
                  },
                  {
                    icon: '🏥',
                    title: 'Saúde Mental',
                    description:
                      'Monitoramento de respostas emocionais em terapias e tratamentos psicológicos.',
                    color: 'from-purple-500 to-purple-600',
                  },
                  {
                    icon: '🎓',
                    title: 'Educação',
                    description:
                      'Estudo de engajamento e atenção em ambientes educacionais e de aprendizagem.',
                    color: 'from-orange-500 to-orange-600',
                  },
                  {
                    icon: '🎮',
                    title: 'Entretenimento',
                    description:
                      'Desenvolvimento de experiências interativas baseadas em respostas emocionais.',
                    color: 'from-pink-500 to-pink-600',
                  },
                  {
                    icon: '👥',
                    title: 'Recursos Humanos',
                    description:
                      'Análise de compatibilidade e respostas emocionais em contextos organizacionais.',
                    color: 'from-indigo-500 to-indigo-600',
                  },
                ].map((app, index) => (
                  <div
                    key={index}
                    className="bg-white dark:bg-[#1e1e1e] rounded-2xl p-6 border border-orange-100 dark:border-orange-900/30 shadow-sm hover:shadow-md transition-all duration-300 group"
                  >
                    <div
                      className={`w-12 h-12 bg-gradient-to-br ${app.color} rounded-xl flex items-center justify-center mb-4 group-hover:scale-110 transition-transform duration-300`}
                    >
                      <span className="text-2xl">{app.icon}</span>
                    </div>
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-3">
                      {app.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300 text-sm leading-relaxed">
                      {app.description}
                    </p>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Team Section */}
          {activeSection === 'team' && (
            <div className="space-y-12">
              <div className="text-center max-w-2xl mx-auto">
                <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                  Equipe do Projeto
                </h2>
                <p className="text-gray-600 dark:text-gray-300">
                  Desenvolvido por estudantes de Ciência da Computação da UTFPR como parte da
                  disciplina de Projeto Integrador.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
                {[
                  {
                    id: 1,
                    name: 'Gabriel Neves',
                    role: 'Dados e sessões EEG',
                    course: 'Ciência da Computação',
                    photo: '/images/gabriel.jpeg',
                  },
                  {
                    id: 2,
                    name: 'Maria Gabriela',
                    role: 'Documentação geral',
                    course: 'Ciência da Computação',
                    photo: '/images/gabi.jpeg',
                  },
                  {
                    id: 3,
                    name: 'Henrique Bittencourt',
                    role: 'Frontend',
                    course: 'Ciência da Computação',
                    photo: '/images/henrique.jpeg',
                  },
                  {
                    id: 4,
                    name: 'Matheus Dalla',
                    role: 'Backend',
                    course: 'Ciência da Computação',
                    photo: '/images/dalla.jpg',
                  },
                ].map((member) => (
                  <div key={member.id} className="text-center group">
                    <div className="relative w-24 h-24 mx-auto mb-4 group">
                      <div className="absolute -inset-1 bg-gradient-to-br from-orange-500 to-amber-600 rounded-full blur-lg opacity-50 group-hover:opacity-75 transition duration-300"></div>
                      <div className="relative w-24 h-24 bg-white dark:bg-gray-800 rounded-full border-2 border-white dark:border-gray-800 overflow-hidden shadow-lg">
                        {member.photo ? (
                          <Image
                            src={member.photo}
                            alt={member.name}
                            width={96}
                            height={96}
                            className="w-full h-full object-cover"
                            placeholder="blur"
                            blurDataURL="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAAIAAoDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAhEAACAQMDBQAAAAAAAAAAAAABAgMABAUGIWGRkqGx0f/EABUBAQEAAAAAAAAAAAAAAAAAAAMF/8QAGhEAAgIDAAAAAAAAAAAAAAAAAAECEgMRkf/aAAwDAQACEQMRAD8AltJagyeH0AthI5xdrLcNM91BF5pX2HaH9bcfaSXWGaRmknyJckliyjqTzSlT54b6bk+h0R"
                          />
                        ) : (
                          <div className="w-full h-full bg-gradient-to-br from-orange-400 to-amber-500 rounded-full flex items-center justify-center">
                            <span className="text-white text-xl font-bold">
                              {member.name
                                .split(' ')
                                .map((n) => n[0])
                                .join('')}
                            </span>
                          </div>
                        )}
                      </div>
                    </div>

                    <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                      {member.name}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-400 text-sm">{member.role}</p>
                    <p className="text-gray-500 dark:text-gray-500 text-xs">{member.course}</p>
                  </div>
                ))}
              </div>

              <div className="bg-gradient-to-br from-orange-50 to-amber-50 dark:from-orange-900/10 dark:to-amber-900/10 rounded-2xl p-8 border border-orange-200 dark:border-orange-800/30">
                <div className="text-center">
                  <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-4">
                    Universidade Tecnológica Federal do Paraná
                  </h3>
                  <p className="text-gray-600 dark:text-gray-300">
                    Este projeto faz parte das atividades acadêmicas do curso de Ciência da
                    Computação, integrando conhecimentos de programação, inteligência artificial e
                    neurociência.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-orange-100 dark:border-orange-900/30 bg-white/80 dark:bg-[#1e1e1e]/80 backdrop-blur-sm mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="text-center">
            <p className="text-gray-600 dark:text-gray-400">
              MANGO - Mindwave Analysis for Neurofeedback & Graphical Observation
            </p>
            <p className="text-gray-500 dark:text-gray-500 text-sm mt-2">
              Projeto Integrador • Ciência da Computação • UTFPR • 2025
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
