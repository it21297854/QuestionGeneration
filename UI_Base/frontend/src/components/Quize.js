import React, { useState, useEffect } from 'react'
import axios from 'axios'

const QuestionDisplay = () => {
  const [questions, setQuestions] = useState([])
  const [userAnswers, setUserAnswers] = useState({})
  const [results, setResults] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [totalScore, setTotalScore] = useState(null)
  const [level, setLevel] = useState(null)

  useEffect(() => {
    fetchLevel()
  }, [])

  const fetchLevel = async () => {
    try {
      const levelResponse = await axios.get('http://127.0.0.1:5000/get_level')
      setLevel(levelResponse.data.level)
    } catch (error) {
      console.error('Error fetching level:', error)
    }
  }

  useEffect(() => {
    if (selectedFile) {
      handleUpload()
    }
  }, [selectedFile])

  const handleFileChange = (event) => {
    const file = event.target.files[0]
    const allowedTypes = [
      'application/pdf',
      'application/msword',
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
      'text/plain',
      'application/vnd.ms-powerpoint',
      'application/vnd.openxmlformats-officedocument.presentationml.presentation',
    ]
    if (!allowedTypes.includes(file.type)) {
      alert(
        'Invalid file type. Please upload a PDF, DOCX, TXT, PPT, or PPTX file.'
      )
      return
    }

    setSelectedFile(file)
  }

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file first!')
      return
    }

    const formData = new FormData()
    formData.append('file', selectedFile)

    try {
      await axios.post('http://127.0.0.1:5000/upload', formData)
      alert('File uploaded successfully! Now generating questions.')
      fetchQuestions()
    } catch (error) {
      console.error('Error uploading file:', error)
    }
  }

  const fetchQuestions = async () => {
    try {
      const response = await axios.get('http://127.0.0.1:5000/get_questions')
      setQuestions(response.data.questions)
    } catch (error) {
      console.error('Error fetching questions:', error)
    }
  }

  const handleAnswerChange = (questionIndex, answer) => {
    setUserAnswers((prev) => ({ ...prev, [questionIndex]: answer }))
  }

  const handleSubmit = async () => {
    try {
      const response = await axios.post(
        'http://127.0.0.1:5000/submit_answers',
        {
          answers: userAnswers,
        }
      )
      setResults(response.data.results)

      // Calculate total score
      const correctAnswers = response.data.results.filter(
        (res) => res.result === 'Correct'
      ).length
      setTotalScore(correctAnswers)
    } catch (error) {
      console.error('Error submitting answers:', error)
    }
  }

  return (
    <div className='container mt-4'>
      <h2 className='mb-4'>AI-based Knowledge {level && ` - ${level}`}</h2>

      {/* File Upload Section */}
      <div className='file-uploader mb-4'>
        <label
          htmlFor='file-upload'
          className='custom-file-upload btn btn-secondary'
        >
          Choose File
        </label>
        <input
          id='file-upload'
          type='file'
          accept='.pdf,.docx,.txt,.ppt,.pptx'
          onChange={handleFileChange}
          className='form-control mt-2'
        />
      </div>

      {/* Display Questions */}
      {questions.length === 0 ? (
        <p>No questions available. Upload a file to generate questions.</p>
      ) : (
        <form className='question-form'>
          {questions.map((q, index) => (
            <div key={index} className='card mb-4 p-3 shadow-sm'>
              <div className='card-body'>
                <h5 className='card-title mb-3'>
                  <strong>Q{index + 1}:</strong> {q.question}
                </h5>
                <div className='options-container'>
                  {q.options.map((option, i) => (
                    <div key={i} className='form-check mb-2'>
                      <input
                        className='form-check-input'
                        type='radio'
                        name={`question_${index}`}
                        value={option}
                        onChange={() => handleAnswerChange(index, option)}
                      />
                      <label className='form-check-label ms-2'>{option}</label>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
          <button
            type='button'
            className='btn btn-primary mt-3'
            onClick={handleSubmit}
          >
            Submit
          </button>
        </form>
      )}

      {/* Display Results */}
      {results && (
        <div className='mt-4'>
          <h3>Results</h3>
          <ul className='list-group'>
            {results.map((res, idx) => (
              <li
                key={idx}
                className={`list-group-item ${
                  res.result === 'Correct' ? 'text-success' : 'text-danger'
                }`}
              >
                <strong>Q{idx + 1}:</strong> {res.question} -{' '}
                <b>{res.result}</b>
                <br />
                <span>
                  Your Answer: <b>{res.user_answer}</b>, Correct:{' '}
                  <b>{res.correct_answer}</b>
                </span>
              </li>
            ))}
          </ul>

          {/* Display Total Score */}
          <div className='mt-3'>
            <h4 className='text-info'>
              Total Score: <b>{totalScore}</b> out of <b>{results.length}</b>
            </h4>
          </div>
        </div>
      )}
    </div>
  )
}

export default QuestionDisplay
