import { useEffect, useRef, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Book, Brain, Music, FileText, ChevronDown, ChevronUp } from 'lucide-react';

function Summary() {
  const location = useLocation();
  const navigate = useNavigate();
  const summary = location.state?.summary;
  const fileName = location.state?.fileName;
  const audioUrl = location.state?.audioUrl;
  const flashcards = location.state?.flashcards;
  const quiz = location.state?.quiz;
  const selectedOptions = location.state?.selectedOptions || {};

  const audioRef = useRef(null);
  const [flippedCards, setFlippedCards] = useState({});
  const [expandedSections, setExpandedSections] = useState({
    summary: true,
    flashcards: true,
    quiz: true,
    audio: true
  });

  console.log("Summary data:", { summary, flashcards, quiz, audioUrl });

  useEffect(() => {
    if (audioRef.current && audioUrl) {
      audioRef.current.load();
      audioRef.current.play().catch((err) => {
        console.warn("Autoplay blocked:", err.message);
      });
    }
  }, [audioUrl]);

  const toggleCard = (index) => {
    setFlippedCards(prev => ({
      ...prev,
      [index]: !prev[index]
    }));
  };

  const toggleSection = (section) => {
    setExpandedSections(prev => ({
      ...prev,
      [section]: !prev[section]
    }));
  };

  // Check if we have any content to display
  const hasContent = summary || (flashcards && flashcards.length > 0) || (quiz && quiz.length > 0) || audioUrl;

  if (!hasContent) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl">⚠️ No content found.</p>
          <button
            onClick={() => navigate('/upload')}
            className="mt-4 bg-primary-500 text-white px-4 py-2 rounded hover:bg-primary-600"
          >
            Back to Upload
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen py-16 px-6 max-w-6xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="space-y-6"
      >
        <h1 className="text-4xl font-bold text-center mb-8 text-gray-900 dark:text-white">
          {fileName || 'Document Results'}
        </h1>

        {/* Summary Section */}
        {summary && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8"
          >
            <button
              onClick={() => toggleSection('summary')}
              className="flex items-center justify-between w-full mb-4"
            >
              <div className="flex items-center gap-3">
                <FileText className="w-6 h-6 text-primary-500" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Summary
                </h2>
              </div>
              {expandedSections.summary ? (
                <ChevronUp className="w-5 h-5" />
              ) : (
                <ChevronDown className="w-5 h-5" />
              )}
            </button>
            {expandedSections.summary && (
              <div className="max-h-[70vh] overflow-y-auto border rounded-md p-4 bg-gray-50 dark:bg-gray-700">
                <p className="whitespace-pre-wrap text-gray-800 dark:text-gray-200 text-lg">
                  {summary}
                </p>
              </div>
            )}
          </motion.div>
        )}

        {/* Audio Section */}
        {audioUrl && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8"
          >
            <button
              onClick={() => toggleSection('audio')}
              className="flex items-center justify-between w-full mb-4"
            >
              <div className="flex items-center gap-3">
                <Music className="w-6 h-6 text-primary-500" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Audio Summary
                </h2>
              </div>
              {expandedSections.audio ? (
                <ChevronUp className="w-5 h-5" />
              ) : (
                <ChevronDown className="w-5 h-5" />
              )}
            </button>
            {expandedSections.audio && (
              <div className="mt-4">
                {audioUrl ? (
                  <audio ref={audioRef} controls className="w-full">
                    <source src={`http://localhost:5000${audioUrl}`} type="audio/mpeg" />
                    Your browser does not support the audio element.
                  </audio>
                ) : (
                  <div className="p-4 bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-800 rounded-lg">
                    <p className="text-yellow-800 dark:text-yellow-200">
                      ⚠️ Audio generation failed. This could be because:
                    </p>
                    <ul className="list-disc list-inside mt-2 text-sm text-yellow-700 dark:text-yellow-300">
                      <li>ELEVENLABS_API_KEY is not set in your .env file</li>
                      <li>API key is invalid or expired</li>
                      <li>Network error occurred during audio generation</li>
                    </ul>
                    <p className="mt-2 text-sm text-yellow-600 dark:text-yellow-400">
                      The summary is still available above. Audio is an optional feature.
                    </p>
                  </div>
                )}
              </div>
            )}
          </motion.div>
        )}

        {/* Flashcards Section */}
        {flashcards && flashcards.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8"
          >
            <button
              onClick={() => toggleSection('flashcards')}
              className="flex items-center justify-between w-full mb-4"
            >
              <div className="flex items-center gap-3">
                <Book className="w-6 h-6 text-primary-500" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Flashcards ({flashcards.length})
                </h2>
              </div>
              {expandedSections.flashcards ? (
                <ChevronUp className="w-5 h-5" />
              ) : (
                <ChevronDown className="w-5 h-5" />
              )}
            </button>
            {expandedSections.flashcards && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                {flashcards.map((card, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, scale: 0.9 }}
                    animate={{ opacity: 1, scale: 1 }}
                    transition={{ delay: index * 0.1 }}
                    onClick={() => toggleCard(index)}
                    className="bg-gradient-to-br from-primary-50 to-primary-100 dark:from-primary-900/20 dark:to-primary-800/20 rounded-lg p-6 cursor-pointer transform transition-transform hover:scale-105 border-2 border-primary-200 dark:border-primary-700 min-h-[200px] flex items-center justify-center"
                  >
                    <div className="text-center w-full">
                      {!flippedCards[index] ? (
                        <div>
                          <p className="text-sm text-primary-600 dark:text-primary-400 mb-2">Question</p>
                          <p className="text-lg font-semibold text-gray-900 dark:text-white">
                            {card.question}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
                            Click to reveal answer
                          </p>
                        </div>
                      ) : (
                        <div>
                          <p className="text-sm text-primary-600 dark:text-primary-400 mb-2">Answer</p>
                          <p className="text-lg text-gray-800 dark:text-gray-200">
                            {card.answer}
                          </p>
                          <p className="text-xs text-gray-500 dark:text-gray-400 mt-4">
                            Click to see question
                          </p>
                        </div>
                      )}
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {/* Quiz Section */}
        {quiz && quiz.length > 0 && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8"
          >
            <button
              onClick={() => toggleSection('quiz')}
              className="flex items-center justify-between w-full mb-4"
            >
              <div className="flex items-center gap-3">
                <Brain className="w-6 h-6 text-primary-500" />
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Quiz Questions ({quiz.length})
                </h2>
              </div>
              {expandedSections.quiz ? (
                <ChevronUp className="w-5 h-5" />
              ) : (
                <ChevronDown className="w-5 h-5" />
              )}
            </button>
            {expandedSections.quiz && (
              <div className="space-y-6 mt-4">
                {quiz.map((item, index) => (
                  <motion.div
                    key={item.id || index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 }}
                    className="bg-gray-50 dark:bg-gray-700 rounded-lg p-6 border border-gray-200 dark:border-gray-600"
                  >
                    <div className="flex items-start gap-3 mb-3">
                      <span className="bg-primary-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold">
                        {item.id || index + 1}
                      </span>
                      <p className="text-lg font-semibold text-gray-900 dark:text-white flex-1">
                        {item.question}
                      </p>
                    </div>
                    <div className="ml-11 mt-3 p-4 bg-white dark:bg-gray-600 rounded border-l-4 border-primary-500">
                      <p className="text-sm text-gray-600 dark:text-gray-300 font-medium mb-1">
                        Answer:
                      </p>
                      <p className="text-gray-800 dark:text-gray-100">
                        {item.correct_answer}
                      </p>
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </motion.div>
        )}

        {/* Navigation Buttons */}
        <div className="flex gap-4 justify-center mt-8">
          <button
            onClick={() => navigate('/upload')}
            className="bg-primary-500 text-white px-6 py-3 rounded-full hover:bg-primary-600 transition-colors font-semibold"
          >
            Upload Another
          </button>
          <button
            onClick={() => navigate('/')}
            className="bg-gray-500 text-white px-6 py-3 rounded-full hover:bg-gray-600 transition-colors font-semibold"
          >
            Go Home
          </button>
        </div>
      </motion.div>
    </div>
  );
}

export default Summary;
