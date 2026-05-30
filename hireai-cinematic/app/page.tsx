"use client";
import { motion } from "framer-motion";
import Lenis from "lenis";
import { useEffect } from "react";
import Scene from "./Scene";
export default function Home() {
  useEffect(() => {
  const lenis = new Lenis();

  function raf(time: number) {
    lenis.raf(time);
    requestAnimationFrame(raf);
  }

  requestAnimationFrame(raf);

  return () => {
    lenis.destroy();
  };
}, []);
  return (
    <main className="min-h-screen bg-black text-white overflow-hidden relative">
{/* Particle Background */}
<div className="absolute inset-0 overflow-hidden">

  {[...Array(40)].map((_, i) => (
    <motion.div
      key={i}
      className="absolute w-1 h-1 bg-cyan-400 rounded-full"
      initial={{
  x: i * 40,
  y: i * 20,
  opacity: 0.2,
}}
      animate={{
        y: [null, -100],
        opacity: [0.2, 1, 0],
      }}
      transition={{
       duration: 5,
repeat: Infinity,
delay: i * 0.2,
      }}
    />
  ))}

</div>
<Scene />
      {/* Animated Background Glow */}
      <div className="absolute top-0 left-0 w-full h-full overflow-hidden">
        <motion.div
          animate={{
            x: [0, 100, -100, 0],
            y: [0, -50, 50, 0],
          }}
          transition={{
            duration: 12,
            repeat: Infinity,
          }}
          className="absolute w-[500px] h-[500px] bg-cyan-500/20 blur-[120px] rounded-full top-[-100px] left-[-100px]"
        />

        <motion.div
          animate={{
            x: [0, -100, 100, 0],
            y: [0, 50, -50, 0],
          }}
          transition={{
            duration: 15,
            repeat: Infinity,
          }}
          className="absolute w-[500px] h-[500px] bg-purple-500/20 blur-[120px] rounded-full bottom-[-100px] right-[-100px]"
        />
      </div>

      {/* Hero Section */}
      <section className="relative z-10 flex flex-col items-center justify-center text-center min-h-screen px-6 overflow-hidden">

  {/* Animated Glow Background */}
  <motion.div
    animate={{
      scale: [1, 1.2, 1],
      opacity: [0.3, 0.6, 0.3],
    }}
    transition={{
      duration: 6,
      repeat: Infinity,
    }}
    className="absolute w-[700px] h-[700px] bg-cyan-500/20 rounded-full blur-[140px]"
  />

  {/* Small Floating Orb */}
  <motion.div
    animate={{
      y: [0, -20, 0],
    }}
    transition={{
      duration: 4,
      repeat: Infinity,
    }}
    className="absolute top-32 right-32 w-32 h-32 bg-cyan-400/30 rounded-full blur-3xl"
  />

  <motion.h1
    initial={{ opacity: 0, y: 100 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ duration: 1 }}
    className="text-7xl md:text-8xl font-black leading-tight tracking-tight"
  >
    FUTURISTIC{" "}
    <span className="text-cyan-400">AI</span>
    <br />
    EXPERIENCE
  </motion.h1>

  <motion.p
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ delay: 0.5 }}
    className="mt-8 text-gray-400 max-w-2xl text-xl"
  >
    AI-powered cinematic hiring platform with futuristic motion,
    intelligent ranking, immersive recruiter workflows and next-gen UI.
  </motion.p>

  <motion.div
    initial={{ opacity: 0, y: 40 }}
    animate={{ opacity: 1, y: 0 }}
    transition={{ delay: 1 }}
    className="flex gap-6 mt-10"
  >
    <button className="px-8 py-4 rounded-full bg-cyan-400 text-black font-bold hover:scale-110 transition">
      Launch AI
    </button>

    <button className="px-8 py-4 rounded-full border border-cyan-400 text-cyan-400 hover:bg-cyan-400 hover:text-black transition">
      View Demo
    </button>
  </motion.div>

</section>
{/* Recruiter Dashboard Section */}

<section className="relative z-10 px-6 py-40">

  <motion.div
    initial={{ opacity: 0, y: 100 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 1 }}
    viewport={{ once: true }}
    className="max-w-7xl mx-auto"
  >

    {/* Heading */}
    <div className="text-center mb-20">
      <h2 className="text-6xl font-black">
        AI RECRUITER{" "}
        <span className="text-cyan-400">
          DASHBOARD
        </span>
      </h2>

      <p className="text-gray-400 mt-6 text-xl max-w-3xl mx-auto">
        Intelligent candidate ranking with futuristic recruiter analytics,
        AI-powered insights and cinematic hiring workflows.
      </p>
    </div>

    {/* Dashboard Grid */}
    <div className="grid grid-cols-1 md:grid-cols-3 gap-8">

      {/* Card 1 */}
      <motion.div
        whileHover={{ scale: 1.03 }}
        className="rounded-3xl border border-cyan-400/20 bg-white/5 backdrop-blur-xl p-8 shadow-[0_0_50px_rgba(34,211,238,0.15)]"
      >
        <h3 className="text-cyan-400 text-2xl font-bold">
          AI Match Score
        </h3>

        <div className="mt-10">
          <div className="h-4 w-full rounded-full bg-black/40 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              whileInView={{ width: "92%" }}
              transition={{ duration: 2 }}
              className="h-full bg-cyan-400"
            />
          </div>

          <p className="mt-4 text-5xl font-black text-white">
            92%
          </p>
        </div>
      </motion.div>

      {/* Card 2 */}
      <motion.div
        whileHover={{ scale: 1.03 }}
        className="rounded-3xl border border-purple-400/20 bg-white/5 backdrop-blur-xl p-8 shadow-[0_0_50px_rgba(168,85,247,0.15)]"
      >
        <h3 className="text-purple-400 text-2xl font-bold">
          Candidates Screened
        </h3>

        <div className="mt-10">
          <p className="text-6xl font-black text-white">
            1.2K
          </p>

          <p className="text-gray-400 mt-4">
            AI-powered resume evaluations processed instantly.
          </p>
        </div>
      </motion.div>

      {/* Card 3 */}
      <motion.div
        whileHover={{ scale: 1.03 }}
        className="rounded-3xl border border-pink-400/20 bg-white/5 backdrop-blur-xl p-8 shadow-[0_0_50px_rgba(236,72,153,0.15)]"
      >
        <h3 className="text-pink-400 text-2xl font-bold">
          Hiring Accuracy
        </h3>

        <div className="mt-10">
          <div className="h-4 w-full rounded-full bg-black/40 overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              whileInView={{ width: "97%" }}
              transition={{ duration: 2 }}
              className="h-full bg-pink-400"
            />
          </div>

          <p className="mt-4 text-5xl font-black text-white">
            97%
          </p>
        </div>
      </motion.div>

    </div>

  </motion.div>

</section>
    </main>
  );
}