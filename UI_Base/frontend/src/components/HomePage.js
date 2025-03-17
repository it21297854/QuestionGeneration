import React from 'react'
import './HomePage.css' // Import external CSS file
import { useNavigate } from 'react-router-dom'

const HomePage = () => {
  return (
    <div className='homepage'>
      <div className='container'>
        <h1>Welcome to the AI Quiz & Answering System</h1>
        <p>
          Welcome to the AI-powered Quiz & Answering System! This platform
          leverages advanced AI technology to generate interactive quizzes
          tailored to your preferences.
        </p>
        <p>
          Whether you're here to test your knowledge, improve your skills, or
          challenge yourself, our system will guide you through a series of fun
          and engaging questions. Each quiz is designed to help you learn and
          assess your understanding of different topics.
        </p>
        <p>
          Simply start by selecting a category or topic, and let the AI generate
          a quiz for you. After you answer the questions, you'll receive
          feedback and explanations for your answers to enhance your learning
          experience.
        </p>
        <p>
          If you need help or have any questions, our support team is ready to
          assist. Dive into the quiz, test your knowledge, and challenge
          yourself with our AI-powered system!
        </p>
        {/* <button
          onClick={
            (() => navigate('/User_Login'), alert('Start Quiz Clicked!'))
          }
        >
          Go to Login
        </button> */}
      </div>
    </div>
  )
}

export default HomePage
