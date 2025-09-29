'use client'

import { Canvas, useLoader } from '@react-three/fiber'
import { OrbitControls, PerspectiveCamera } from '@react-three/drei'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader'
import { Suspense, useRef } from 'react'
import * as THREE from 'three'

function Model({ url, scale = [1, 1, 1] }) {
  const gltf = useLoader(GLTFLoader, url)
  return <primitive object={gltf.scene} scale={scale} />
}

function Loading() {
  return (
    <mesh rotation={[0, 0, 0]}>
      <boxGeometry args={[1, 1, 1]} />
      <meshStandardMaterial color="#3b82f6" wireframe />
    </mesh>
  )
}

export default function SimpleModelViewer({
  modelPath,
  className = 'w-full h-96 dark:bg-[#101111] bg-white',
}) {
  const controlsRef = useRef()

  return (
    <div className={className}>
      <Canvas gl={{ alpha: true }}>
        <ambientLight intensity={0.7} />
        <directionalLight position={[5, 5, 5]} intensity={0.8} castShadow />
        <spotLight position={[-5, 5, 5]} angle={0.3} penumbra={1} intensity={0.5} />
        <PerspectiveCamera makeDefault position={[0, 0, 6]} fov={45} />
        <Suspense fallback={<Loading />}>
          <Model url={modelPath} scale={[2, 2, 2]} />
        </Suspense>
        <OrbitControls
          ref={controlsRef}
          enablePan={false}
          enableZoom={true}
          enableRotate={true}
          minDistance={6}
          maxDistance={10}
          minPolarAngle={0}
          maxPolarAngle={Math.PI}
          mouseButtons={{
            LEFT: THREE.MOUSE.ROTATE,
            MIDDLE: THREE.MOUSE.DOLLY,
            RIGHT: null,
          }}
          touches={{
            ONE: THREE.TOUCH.ROTATE,
            TWO: THREE.TOUCH.DOLLY,
          }}
          enableDamping={true}
          dampingFactor={0.1}
          rotateSpeed={0.5}
          zoomSpeed={0.8}
          target={[0, 0, 0]}
        />
      </Canvas>
    </div>
  )
}
