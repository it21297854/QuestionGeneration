import React from "react";
import styles from "./QuestionModal.module.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function QuestionModal({ question, onClose }) {
  if (!question) return null;

  return (
    <div className={styles.modalOverlay} onClick={onClose}>
      <div className={styles.modalContent} onClick={(e) => e.stopPropagation()}>
        {/* Close Button */}
        <button className={styles.closeButton} onClick={onClose}>
          &times;
        </button>

        {/* Question Meta Info */}
        <div className={styles.questionMeta}>
          <span className={`${styles.questionType} ${styles[question.question_type]}`}>
            {question.question_type.replace("-", " ")}
          </span>
          <span className={`${styles.language} ${styles[question.language]}`}>
            {question.language.charAt(0).toUpperCase() + question.language.slice(1)}
          </span>
          <span className={`${styles.difficulty} ${styles[question.difficulty]}`}>
            {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
          </span>
        </div>

        {/* Question Title */}
        <h3 className={styles.questionTitle}>{question.description}</h3>

        {/* If it's an MCQ, show options */}
        {question.question_type === "mcq" && (
          <ul className={styles.mcqOptions}>
            {question.options.map((option, index) => (
              <li key={index} className={styles.mcqOption}>
                {index + 1}. {option}
              </li>
            ))}
          </ul>
        )}

        {/* Show Answer Button */}
        <button
          className={styles.answerButton}
          onClick={() => document.getElementById("answerSection").classList.toggle(styles.show)}
        >
          Show Answer
        </button>

        {/* Display Answer */}
        <div id="answerSection" className={styles.answerSection}>
          {question.question_type === "coding" ? (
            <SyntaxHighlighter language={question.language} style={atomDark} className={styles.codeBlock}>
              {question.code_snippet || "No code available"}
            </SyntaxHighlighter>
          ) : (
            <p className={styles.answerText}>
              Correct Answer: {question.question_type === "mcq" ? question.correct_option : question.expected_answers}
            </p>
          )}
        </div>
      </div>
    </div>
  );
}

export default QuestionModal;
