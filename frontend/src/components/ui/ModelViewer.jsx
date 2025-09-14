'use client'

import { Canvas, useFrame, useLoader } from '@react-three/fiber'
import { OrbitControls } from '@react-three/drei'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { Suspense } from 'react'

function Model({ url, scale = [1, 1, 1] }) {
  const gltf = useLoader(GLTFLoader, url)
  return <primitive object={gltf.scene} scale={scale} />
}

function Loading() {
  return (
    <mesh>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="blue" />
    </mesh>
  )
}

export default function SimpleModelViewer({ modelPath }) {
  return (
    <div style={{ width: '800px', height: '500px' }}>
      <Canvas>
        <ambientLight intensity={2} />
        <spotLight position={[10, 10, 10]} angle={90} penumbra={1} />
        <Suspense fallback={<Loading />}>
          {/* aqui define a escala inicial */}
          <Model url={modelPath} scale={[2, 2, 2]} />
        </Suspense>
        <OrbitControls />
      </Canvas>
    </div>
  )
}
