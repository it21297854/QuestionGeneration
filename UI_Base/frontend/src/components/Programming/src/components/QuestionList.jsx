import React, { useState } from "react";
import styles from './QuestionList.module.css';
import QuestionItem from "./QuestionItem";
import QuestionModal from "./QuestionModal";

function QuestionList({ questions, setFilters }) {
    const [selectedQuestion, setSelectedQuestion] = useState(null);

    const handleFilterChange = (e) => {
      setFilters((prevFilters) => ({
        ...prevFilters,
        [e.target.name]: e.target.value,
      }));
    };

    return (
        <div className={styles.container}>
          <h2 className={styles.title}>Programming Questions</h2>
    
          {/* Filter Section */}
          <div className={styles["filter-section"]}>
            <select name="language" className={styles.select} onChange={handleFilterChange}>
              <option value="">All Languages</option>
              <option value="python">Python</option>
              <option value="java">Java</option>
              <option value="javascript">JavaScript</option>
            </select>
            <select name="type" className={styles.select} onChange={handleFilterChange}>
              <option value="">All Types</option>
              <option value="mcq">MCQ</option>
              <option value="short-answer">Short Answer</option>
              <option value="coding">Coding</option>
            </select>
            <select name="difficulty" className={styles.select} onChange={handleFilterChange}>
              <option value="">All Difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
    
          {/* Question List */}
          <div className={styles["question-list"]}>
            {questions.length > 0 ? (
              questions.map((q, index) => (
                <div key={index} className={styles["question-item"]} onClick={() => setSelectedQuestion(q)}>
                  <div className={styles["question-meta"]}>
                    <span className={`${styles["question-type"]} ${styles[q.question_type]}`}>
                    {q.question_type.replace("-", " ")}
                    </span>
                    <span className={`${styles["language"]} ${styles[q.language]}`}>
                    {q.language.charAt(0).toUpperCase() + q.language.slice(1)}
                    </span>
                    <span className={`${styles["difficulty"]} ${styles[q.difficulty]}`}>
                    {q.difficulty.charAt(0).toUpperCase() + q.difficulty.slice(1)}
                    </span>
                    </div>
                  <h3 className={styles["question-title"]}>{q.description}</h3>
                  {/* <p className={styles["question-meta"]}>
                    Type: {q.question_type} | Difficulty: {q.difficulty} | Language: {q.language}
                  </p> */}
                </div>
              ))
            ) : (
              <p className={styles["no-questions"]}>No questions found.</p>
            )}
          </div>
          {/* Modal for Selected Question
      {selectedQuestion && (
        <div className={styles.modal} onClick={() => setSelectedQuestion(null)}>
          <div className={styles["modal-content"]} onClick={(e) => e.stopPropagation()}>
            <button className={styles["close-button"]} onClick={() => setSelectedQuestion(null)}>×</button>
            <QuestionItem question={selectedQuestion} />
          </div>
        </div>
      )} */}
      {/* Modal */}
      {selectedQuestion && <QuestionModal question={selectedQuestion} onClose={() => setSelectedQuestion(null)} />}
        </div>
      );
  
    // return (
    //   <div className="max-w-2xl mx-auto bg-white p-5 rounded shadow">
    //     <h2 className="text-xl font-bold mb-4">Question History</h2>
  
    //     {/* Filter Section */}
    //     <div className="grid grid-cols-3 gap-3 mb-4">
    //       <select name="language" className="p-2 border rounded" onChange={handleFilterChange}>
    //         <option value="">All Languages</option>
    //         <option value="python">Python</option>
    //         <option value="java">Java</option>
    //         <option value="javascript">JavaScript</option>
    //       </select>
    //       <select name="type" className="p-2 border rounded" onChange={handleFilterChange}>
    //         <option value="">All Types</option>
    //         <option value="mcq">MCQ</option>
    //         <option value="short-answer">Short Answer</option>
    //         <option value="coding">Coding</option>
    //       </select>
    //       <select name="difficulty" className="p-2 border rounded" onChange={handleFilterChange}>
    //         <option value="">All Difficulties</option>
    //         <option value="easy">Easy</option>
    //         <option value="medium">Medium</option>
    //         <option value="hard">Hard</option>
    //       </select>
    //     </div>
  
    //     {/* Question List */}
    //     <div className="space-y-4">
    //       {questions.length > 0 ? (
    //         questions.map((q, index) => (
    //           <div key={index} className="p-3 border rounded bg-gray-50">
    //             <h3 className="font-semibold">{q.text}</h3>
    //             <p className="text-sm text-gray-500">Type: {q.question_type} | Difficulty: {q.difficulty} | Language: {q.language}</p>
    //           </div>
    //         ))
    //       ) : (
    //         <p className="text-gray-500">No questions found.</p>
    //       )}
    //     </div>
    //   </div>
    // );
  }
  
  export default QuestionList;
  