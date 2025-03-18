import React, { useState } from 'react';
import styles from './QuestionForm.module.css';

const QuestionForm = ({ onSubmit }) => {
  const [topic, setTopic] = useState('');
  const [type, setType] = useState('mcq');
  const [difficulty, setDifficulty] = useState('easy');
  const [language, setLanguage] = useState('python');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ topic, type, difficulty, language });
  };

  return (
    <div className={styles['form-container']}>
      <h2>Generate a Question</h2>
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label>Topic</label>
          <input type="text" value={topic} onChange={(e) => setTopic(e.target.value)} />
        </div>

        <div className="form-group">
          <label>Type</label>
          <select value={type} onChange={(e) => setType(e.target.value)}>
            <option value="mcq">MCQ</option>
            <option value="short-answer">Short Answer</option>
            <option value="coding">Coding</option>
          </select>
        </div>

        <div className="form-group">
          <label>Difficulty</label>
          <select value={difficulty} onChange={(e) => setDifficulty(e.target.value)}>
            <option value="easy">Easy</option>
            <option value="medium">Medium</option>
            <option value="hard">Hard</option>
          </select>
        </div>

        <div className="form-group">
          <label>Language</label>
          <select value={language} onChange={(e) => setLanguage(e.target.value)}>
            <option value="python">Python</option>
            <option value="java">Java</option>
            <option value="javascript">JavaScript</option>
          </select>
        </div>

        <button className={styles['submit-button']} type="submit">Generate</button>
      </form>
    </div>
  );
};

export default QuestionForm;
