import React from 'react';

const HomePage = () => {
  return (
    <div
      className="homepage"
      style={{
        minHeight: '100vh',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        
        padding: '20px',
      }}
    >
      <div
        className="container"
        style={{
          backgroundColor: 'rgba(0, 0, 0, 0.6)',  
          padding: '30px',
          borderRadius: '8px',
          color: '#ffffff',  
          maxWidth: '800px', // Limit the width to make the card more focused
          textAlign: 'center',
        }}
      >
        <h1>Welcome to the AI Quiz & Answering System</h1>
        <br /><br />
        <p>
          Welcome to the AI-powered Quiz & Answering System! This platform leverages advanced AI technology to generate interactive quizzes tailored to your preferences. 
        </p>
        <p>
          Whether you're here to test your knowledge, improve your skills, or challenge yourself, our system will guide you through a series of fun and engaging questions. Each quiz is designed to help you learn and assess your understanding of different topics.
        </p>
        <p>
          Simply start by selecting a category or topic, and let the AI generate a quiz for you. After you answer the questions, you'll receive feedback and explanations for your answers to enhance your learning experience.
        </p>
        <p>
          If you need help or have any questions, our support team is ready to assist. Dive into the quiz, test your knowledge, and challenge yourself with our AI-powered system!
        </p>
      </div>
    </div>
  );
};

export default HomePage;
