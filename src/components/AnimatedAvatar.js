import React from 'react';
import { motion } from 'framer-motion';

const AnimatedAvatar = ({ persona, isSpeaking, size = 'large' }) => {
  const sizeClasses = {
    small: 'w-12 h-12',
    medium: 'w-20 h-20',
    large: 'w-32 h-32'
  };

  const isCFO = persona === 'CFO';
  const isCEO = persona === 'CEO';

  return (
    <div className="relative flex flex-col items-center">
      {/* Clean Professional Avatar */}
      <motion.div
        className={`${sizeClasses[size]} relative`}
        style={{
          perspective: '1000px',
          transformStyle: 'preserve-3d'
        }}
        animate={{
          rotateY: isSpeaking ? [0, 1, -1, 0] : 0,
          scale: isSpeaking ? [1, 1.01, 1] : 1,
        }}
        transition={{
          duration: 2,
          repeat: isSpeaking ? Infinity : 0,
          ease: "easeInOut"
        }}
      >
        {/* Main Avatar Circle */}
        <div className="absolute inset-0 rounded-full overflow-hidden">
          {/* Background Gradient */}
          <motion.div
            className={`absolute inset-0 rounded-full ${
              isCFO 
                ? 'bg-gradient-to-br from-slate-600 via-slate-700 to-slate-800' 
                : 'bg-gradient-to-br from-indigo-600 via-indigo-700 to-indigo-800'
            }`}
            animate={{
              opacity: isSpeaking ? [0.9, 1, 0.9] : 0.95,
            }}
            transition={{
              duration: 2,
              repeat: isSpeaking ? Infinity : 0,
              ease: "easeInOut"
            }}
          />
          
          {/* Inner Circle */}
          <div className={`absolute inset-1 rounded-full ${
            isCFO 
              ? 'bg-gradient-to-br from-slate-500 to-slate-600' 
              : 'bg-gradient-to-br from-indigo-500 to-indigo-600'
          }`} />
          
          {/* Face Area */}
          <div className="absolute inset-2 rounded-full bg-gradient-to-br from-gray-100 to-gray-200 flex items-center justify-center">
            
            {/* Professional Hair */}
            <div className="absolute -top-2 left-1/2 transform -translate-x-1/2">
              <div className={`w-8 h-4 rounded-full ${
                isCFO ? 'bg-gradient-to-br from-gray-800 to-gray-900' : 'bg-gradient-to-br from-gray-700 to-gray-800'
              }`} />
            </div>
            
            {/* Professional Eyes */}
            <div className="absolute top-1/3 left-1/2 transform -translate-x-1/2">
              <div className="flex space-x-3">
                <motion.div
                  className="w-3 h-3 bg-white rounded-full border border-gray-300 shadow-sm"
                  animate={{
                    scaleY: isSpeaking ? [1, 0.1, 1] : 1,
                  }}
                  transition={{
                    duration: 0.3,
                    repeat: isSpeaking ? Infinity : 0,
                    ease: "easeInOut"
                  }}
                >
                  <div className="w-1.5 h-1.5 bg-gray-800 rounded-full mt-0.5 ml-0.5" />
                </motion.div>
                <motion.div
                  className="w-3 h-3 bg-white rounded-full border border-gray-300 shadow-sm"
                  animate={{
                    scaleY: isSpeaking ? [1, 0.1, 1] : 1,
                  }}
                  transition={{
                    duration: 0.3,
                    repeat: isSpeaking ? Infinity : 0,
                    ease: "easeInOut",
                    delay: 0.1
                  }}
                >
                  <div className="w-1.5 h-1.5 bg-gray-800 rounded-full mt-0.5 ml-0.5" />
                </motion.div>
              </div>
            </div>
            
            {/* Professional Nose */}
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 w-1 h-1 bg-gray-400 rounded-full" />
            
            {/* Professional Mouth */}
            <motion.div
              className="absolute bottom-1/4 left-1/2 transform -translate-x-1/2"
              animate={{
                scaleY: isSpeaking ? [1, 0.2, 1] : 1,
                scaleX: isSpeaking ? [1, 1.1, 1] : 1,
              }}
              transition={{
                duration: 0.4,
                repeat: isSpeaking ? Infinity : 0,
                ease: "easeInOut"
              }}
            >
              <div className="w-4 h-2 bg-gray-300 rounded-full border border-gray-400" />
            </motion.div>
          </div>
          
          {/* Professional Tie */}
          <div className="absolute bottom-1 left-1/2 transform -translate-x-1/2">
            <div className={`w-1 h-4 rounded-sm ${
              isCFO ? 'bg-red-600' : 'bg-blue-600'
            }`} />
          </div>
        </div>

        {/* Subtle Professional Glow */}
        <motion.div
          className={`absolute inset-0 rounded-full ${
            isCFO 
              ? 'shadow-slate-500/20' 
              : 'shadow-indigo-500/20'
          } shadow-lg`}
          animate={{
            boxShadow: isSpeaking 
              ? [
                  `0 0 20px ${isCFO ? 'rgba(71, 85, 105, 0.3)' : 'rgba(79, 70, 229, 0.3)'}`,
                  `0 0 30px ${isCFO ? 'rgba(71, 85, 105, 0.4)' : 'rgba(79, 70, 229, 0.4)'}`,
                  `0 0 20px ${isCFO ? 'rgba(71, 85, 105, 0.3)' : 'rgba(79, 70, 229, 0.3)'}`
                ]
              : `0 0 10px ${isCFO ? 'rgba(71, 85, 105, 0.2)' : 'rgba(79, 70, 229, 0.2)'}`
          }}
          transition={{
            duration: 2,
            repeat: isSpeaking ? Infinity : 0,
            ease: "easeInOut"
          }}
        />

        {/* Professional Speech Indicators */}
        {isSpeaking && (
          <>
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                className="absolute text-xs text-gray-600 opacity-60"
                animate={{
                  y: [0, -40],
                  x: [0, Math.random() * 20 - 10],
                  opacity: [0, 0.6, 0],
                  scale: [0.5, 0.8, 0.5],
                }}
                transition={{
                  duration: 2,
                  repeat: Infinity,
                  ease: "easeOut",
                  delay: i * 0.4
                }}
                style={{
                  left: '50%',
                  top: '50%',
                }}
              >
                {['💬', '🗣️', '✨'][i]}
              </motion.div>
            ))}
          </>
        )}
      </motion.div>

      {/* Clean Professional Name Badge */}
      <motion.div
        className="mt-4"
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div className={`px-4 py-2 rounded-lg text-sm font-medium text-white shadow-md ${
          isCFO 
            ? 'bg-gradient-to-r from-slate-600 to-slate-700' 
            : 'bg-gradient-to-r from-indigo-600 to-indigo-700'
        }`}>
          {persona}
        </div>
      </motion.div>

      {/* Professional Status Indicator */}
      <motion.div
        className="mt-2 flex items-center space-x-2"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.7 }}
      >
        <motion.div
          className={`w-2 h-2 rounded-full ${
            isSpeaking ? 'bg-green-500' : 'bg-gray-400'
          }`}
          animate={{
            scale: isSpeaking ? [1, 1.1, 1] : 1,
            opacity: isSpeaking ? [0.8, 1, 0.8] : 0.8,
          }}
          transition={{
            duration: 1,
            repeat: isSpeaking ? Infinity : 0,
            ease: "easeInOut"
          }}
        />
        <span className="text-xs text-gray-500 font-medium">
          {isSpeaking ? 'Speaking' : 'Online'}
        </span>
      </motion.div>
    </div>
  );
};

export default AnimatedAvatar;
