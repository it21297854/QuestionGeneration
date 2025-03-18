import { useState } from "react";
import styles from "./QuestionItem.module.css";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { atomDark } from "react-syntax-highlighter/dist/esm/styles/prism";

function QuestionItem({ question }) {
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div className={styles["question-container"]}>
      {/* Question Meta Info */}
      <div className={styles["question-meta"]}>
        <span className={`${styles["question-type"]} ${styles[question.question_type]}`}>
          {question.question_type.replace("-", " ")}
        </span>
        <span className={`${styles["language"]} ${styles[question.language]}`}>
            {question.language.charAt(0).toUpperCase() + question.language.slice(1)}
        </span>
        <span className={`${styles["difficulty"]} ${styles[question.difficulty]}`}>
          {question.difficulty.charAt(0).toUpperCase() + question.difficulty.slice(1)}
        </span>
      </div>

      {/* Question Title */}
      <h3 className={styles["question-text"]}>{question.description}</h3>

      {/* If it's an MCQ, show options */}
      {question.question_type === "mcq" && (
        <ul className={styles["mcq-options"]}>
          {question.options.map((option, index) => (
            <li key={index} className={styles["mcq-option"]}>
              {index + 1}. {option}
            </li>
          ))}
        </ul>
      )}

      {/* Show Answer Button */}
      <button
        onClick={() => setShowAnswer(!showAnswer)}
        className={styles["answer-button"]}
      >
        {showAnswer ? "Hide Answer" : "Show Answer"}
      </button>

      {/* Display Answer when button is clicked */}
      {showAnswer && (
        question.question_type === "coding" ? (
        //   <pre className={styles["code-block"]}>
        //     <code>{question.code_snippet}</code>
        //   </pre>
        <SyntaxHighlighter language={question.language} style={atomDark} className={styles["code-block"]}>
            {question.code_snippet}
          </SyntaxHighlighter>
        ) : (
        <p className={styles["answer-text"]}>
          Correct Answer: {question.question_type == 'mcq'? question.correct_option: question.expected_answers}
        </p>
        )
      )}
    </div>
  );
//   return (
//     <div className={styles["question-container"]}>
//       <h3 className={styles["question-text"]}>{question.description}</h3>
//       <button
//         onClick={() => setShowAnswer(!showAnswer)}
//         className={styles["answer-button"]}
//       >
//         {showAnswer ? "Hide Answer" : "Show Answer"}
//       </button>
//       {showAnswer && <p className={styles["answer-text"]}>{question.correct_option}</p>}
//     </div>
//   );
}

export default QuestionItem;
