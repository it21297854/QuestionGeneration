import React from "react";
import { useState } from "react";
import { fetchQuestion } from "../apis/api";
import QuestionItem from "../components/QuestionItem";
import styles from "./Home.module.css";

function Home() {
  const [formData, setFormData] = useState({
    topic: "",
    type: "mcq",
    difficulty: "easy",
    language: "python",
  });
  const [question, setQuestion] = useState(null);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await fetchQuestion(formData);
      setQuestion(data);
    } catch (error) {
      alert("Failed to fetch question: " + error);
    }
  };

  return (
    <div className={styles["home-container"]}>
      <h2 className={styles.title}>Generate Programming Question</h2>
      <form onSubmit={handleSubmit} className={styles.form}>
        <div style={{width: '100%'}}>
            <input
            type="text"
            name="topic"
            placeholder="Enter topic"
            className={styles.input}
            onChange={handleChange}
            required
            /> 
        </div>
        <div className={styles["select-divs"]}>
            <div style={{width: '100%'}}>
                <select name="type" className={styles.select} onChange={handleChange}>
                    <option value="mcq">MCQ</option>
                    <option value="short-answer">Short Answer</option>
                    <option value="coding">Coding</option>
                </select>
            </div>
            <div style={{width: '100%'}}>
                <select name="difficulty" className={styles.select} onChange={handleChange}>
                    <option value="easy">Easy</option>
                    <option value="medium">Medium</option>
                    <option value="hard">Hard</option>
                </select>
            </div>
            <div style={{width: '100%'}}>
                <select name="language" className={styles.select} onChange={handleChange}>
                    <option value="python">Python</option>
                    <option value="java">Java</option>
                    <option value="javascript">JavaScript</option>
                </select>
            </div>
        </div>
        
        <button type="submit" className={styles.button}>Generate</button>
      </form>
      {question && <QuestionItem question={question} />}
    </div>
  );
}

export default Home;
