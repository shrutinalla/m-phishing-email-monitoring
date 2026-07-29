import { useState } from "react";
import "./Quiz.css";
import { awarenessQuiz } from "../../Data/awarenessData";

function Quiz() {
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState(null);
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const question = awarenessQuiz[currentQuestion];

  const handleSubmit = () => {
    if (selectedAnswer === null) return;

    if (selectedAnswer === question.correctAnswer) {
      setScore((prev) => prev + 1);
    }

    setSubmitted(true);
  };

  const handleNext = () => {
    if (currentQuestion < awarenessQuiz.length - 1) {
      setCurrentQuestion((prev) => prev + 1);
      setSelectedAnswer(null);
      setSubmitted(false);
    }
  };

  const handleRestart = () => {
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setSubmitted(false);
    setScore(0);
  };

  const quizFinished =
    currentQuestion === awarenessQuiz.length - 1 && submitted;

  return (
    <div className="quiz-card">

      {quizFinished ? (

        <div className="score-card">

          <h2>🎉 Quiz Completed</h2>

          <h3>
            Your Score: {score} / {awarenessQuiz.length}
          </h3>

          <button
            className="quiz-btn"
            onClick={handleRestart}
          >
            Restart Quiz
          </button>

        </div>

      ) : (

        <>

          <div className="quiz-header">

            <h2>Interactive Security Quiz</h2>

            <span>
              Question {currentQuestion + 1} of {awarenessQuiz.length}
            </span>

          </div>

          <h3 className="question">
            {question.question}
          </h3>

          <div className="options">

            {question.options.map((option, index) => (

              <button
                key={index}
                className={`option
                  ${selectedAnswer === index ? "selected" : ""}
                  ${
                    submitted && index === question.correctAnswer
                      ? "correct"
                      : ""
                  }
                  ${
                    submitted &&
                    selectedAnswer === index &&
                    selectedAnswer !== question.correctAnswer
                      ? "wrong"
                      : ""
                  }`}
                disabled={submitted}
                onClick={() => setSelectedAnswer(index)}
              >
                {option}
              </button>

            ))}

          </div>

          {!submitted ? (

            <button
              className="quiz-btn"
              onClick={handleSubmit}
            >
              Submit Answer
            </button>

          ) : (

            <>

              <div className="explanation">

                <strong>Explanation</strong>

                <p>{question.explanation}</p>

              </div>

              <button
                className="quiz-btn"
                onClick={handleNext}
              >
                Next Question
              </button>

            </>

          )}

        </>

      )}

    </div>
  );
}

export default Quiz;