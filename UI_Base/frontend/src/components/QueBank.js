import React, { useState, useEffect } from 'react'
import './QueBank.css' // Make sure to create a CSS file for styles

const QueBank = () => {
  const [questions, setQuestions] = useState([])
  const [difficulty, setDifficulty] = useState('Low Level') // Default difficulty set to 'Low Level'
  const [error, setError] = useState(null)

  const fetchQuestions = async (selectedDifficulty) => {
    try {
      const response = await fetch(
        `http://127.0.0.1:5000/get_questions_by_difficulty?difficulty=${selectedDifficulty}`
      )
      const data = await response.json()

      if (response.ok) {
        setQuestions(data.questions)
        setError(null) // Clear any previous errors
      } else {
        setError(data.message || 'Error fetching questions')
        setQuestions([])
      }
    } catch (error) {
      setError('Failed to fetch questions')
      setQuestions([])
    }
  }

  useEffect(() => {
    fetchQuestions(difficulty) // Fetch questions when the difficulty changes
  }, [difficulty])

  return (
    <div className='que-bank-container'>
      <header>
        <h1>Welcome to the Question Bank</h1>
        <p>Select a difficulty level to start exploring the questions!</p>
      </header>

      <div className='difficulty-selection'>
        <label>Select Difficulty Level:</label>
        <select
          value={difficulty}
          onChange={(e) => setDifficulty(e.target.value)}
          className='difficulty-dropdown'
        >
          <option value='Low Level'>Low Level</option>
          <option value='Medium Level'>Medium Level</option>
          <option value='High Level'>High Level</option>
        </select>
      </div>

      {error && <p className='error-message'>{error}</p>}

      <section className='questions-section'>
        <h2>Questions for {difficulty}</h2>
        {questions.length > 0 ? (
          <ul className='question-list'>
            {questions.map((question, index) => (
              <li key={index} className='question-item'>
                <p className='question-text'>
                  <strong>{question.question}</strong>
                </p>
                <p>
                  <strong>Answer:</strong> {question.correct_answer}
                </p>
              </li>
            ))}
          </ul>
        ) : (
          <p>No questions available for the selected difficulty.</p>
        )}
      </section>
    </div>
  )
}

export default QueBank
