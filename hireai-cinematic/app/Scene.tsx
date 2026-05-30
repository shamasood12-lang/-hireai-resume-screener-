"use client";

import { Canvas, useFrame } from "@react-three/fiber";
import { Float, Stars } from "@react-three/drei";
import { useRef } from "react";
import * as THREE from "three";

function AnimatedSphere({
  position,
  color,
  scale,
}: {
  position: [number, number, number];
  color: string;
  scale: number;
}) {
  const meshRef = useRef<THREE.Mesh>(null!);

  useFrame((state) => {
    if (!meshRef.current) return;

    meshRef.current.rotation.x += 0.002;
    meshRef.current.rotation.y += 0.003;

    meshRef.current.position.y =
      position[1] + Math.sin(state.clock.elapsedTime) * 0.2;
  });

  return (
    <Float speed={2} rotationIntensity={2} floatIntensity={2}>
      <mesh ref={meshRef} position={position} scale={scale}>
        <icosahedronGeometry args={[2, 1]} />

        <meshStandardMaterial
          color={color}
          emissive={color}
          emissiveIntensity={2}
          wireframe
        />
      </mesh>
    </Float>
  );
}

export default function Scene() {
  return (
    <div className="absolute inset-0 z-0">
      <Canvas camera={{ position: [0, 0, 12] }}>

        {/* Lighting */}
        <ambientLight intensity={1.5} />

        <pointLight position={[10, 10, 10]} intensity={5} />

        <pointLight position={[-10, -10, -10]} intensity={3} />

        {/* Stars Background */}
        <Stars
          radius={100}
          depth={50}
          count={1500}
          factor={2}
          saturation={0}
          fade
          speed={1}
        />

        {/* Main Orb */}
        <AnimatedSphere
          position={[4, -1, 0]}
          color="#00e5ff"
          scale={1.5}
        />

        {/* Secondary Orb */}
        <AnimatedSphere
          position={[-4, 2, -2]}
          color="#a855f7"
          scale={0.8}
        />

        {/* Small Orb */}
        <AnimatedSphere
          position={[0, 3, -4]}
          color="#ec4899"
          scale={0.5}
        />

      </Canvas>
    </div>
  );
}