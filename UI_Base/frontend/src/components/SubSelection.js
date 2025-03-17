import React from 'react'
import { useNavigate } from 'react-router-dom'

const Subjects = () => {
  const navigate = useNavigate()

  const handleSubjectClick = (subject) => {
    navigate(`/Quize/${subject.toLowerCase()}`) // Navigate to the quiz page for the selected subject
  }

  return (
    <div
      className='container mt-4 text-center'
      style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        flexDirection: 'column',
        gap: '20px', // Adds spacing between buttons
        textAlign: 'center',
      }}
    >
      <h2 className='mb-4'>Select a Subject</h2>
      <div
        style={{
          display: 'flex',
          gap: '15px', // Adds vertical spacing between buttons
        }}
      >
        <button
          className='btn subject-btn'
          onClick={() => handleSubjectClick('Software Engineering')}
        >
          Software Engineering
        </button>
        <button
          className='btn subject-btn'
          onClick={() => handleSubjectClick('English')}
        >
          English
        </button>
        <button
          className='btn subject-btn'
          onClick={() => handleSubjectClick('Maths')}
        >
          Maths
        </button>
        <button
          className='btn subject-btn'
          onClick={() => handleSubjectClick('Programming')}
        >
          Programming
        </button>
      </div>
    </div>
  )
}

export default Subjects
