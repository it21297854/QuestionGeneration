import React, { useState, useEffect } from 'react';
import axios from 'axios';

const QuestionDisplay = () => {
    const [questions, setQuestions] = useState([]);
    const [userAnswers, setUserAnswers] = useState({});
    const [results, setResults] = useState(null);
    const [selectedFile, setSelectedFile] = useState(null);
    const [totalScore, setTotalScore] = useState(null);
    const [level, setLevel] = useState("");


    useEffect(() => {
        fetchLevel();
    }, []);


    const fetchLevel = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5001/get_level');
            if (response.data.level) {
                setLevel(response.data.level);
            } else {
                console.error("No level found in response:", response.data);
            }
        } catch (error) {
            console.error('Error fetching level:', error);
        }
    };


    const handleFileChange = (event) => {
        const file = event.target.files[0];
        const allowedTypes = ['application/pdf', 'application/msword', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'text/plain', 'application/vnd.ms-powerpoint', 'application/vnd.openxmlformats-officedocument.presentationml.presentation'];
        if (!allowedTypes.includes(file.type)) {
            alert('Invalid file type. Please upload a PDF, DOCX, TXT, PPT, or PPTX file.');
            return;
        }
        setSelectedFile(file);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Please select a file first!");
            return;
        }

        const formData = new FormData();
        formData.append("file", selectedFile);

        try {
            await axios.post('http://127.0.0.1:5001/upload', formData);
            alert("File uploaded successfully! Now generating questions.");
            fetchQuestions();
        } catch (error) {
            console.error("Error uploading file:", error);
        }
    };


    const fetchQuestions = async () => {
        try {
            const response = await axios.get('http://127.0.0.1:5001/get_questions');
            setQuestions(response.data.questions);
        } catch (error) {
            console.error('Error fetching questions:', error);
        }
    };


    const handleAnswerChange = (questionIndex, answer) => {
        setUserAnswers(prev => ({ ...prev, [questionIndex]: answer }));
    };


    const handleSubmit = async () => {
        try {
            const response = await axios.post('http://127.0.0.1:5001/submit_answers', { answers: userAnswers });
            setResults(response.data.results);


            const correctAnswers = response.data.results.filter(res => res.result === 'Correct').length;
            setTotalScore(correctAnswers);


            fetchLevel();
        } catch (error) {
            console.error('Error submitting answers:', error);
        }
    };

    return (
        <div className="container mt-4">
            <h2 className="mb-4">
                AI-based Knowledge {level && `- ${level}`}
            </h2>

            {/* File Upload Section */}
            <div className="file-uploader">
                <label htmlFor="file-upload" className="custom-file-upload">
                    <i className="fas fa-file-upload"></i> Choose File
                </label>
                <input
                    id="file-upload"
                    type="file"
                    accept=".pdf,.docx,.txt,.ppt,.pptx"
                    onChange={handleFileChange}
                />
                <button onClick={handleUpload} className="btn btn-upload">
                    <i className="fas fa-upload"></i> Upload File
                </button>
            </div>

            {/* Display Questions */}
            {questions.length === 0 ? (
                <p>No questions available. Upload a file to generate questions.</p>
            ) : (
                <form>
                    {questions.map((q, index) => (
                        <div key={index} className="card mb-3">
                            <div className="card-body">
                                <h5 className="card-title">{index + 1}. {q.question}</h5>
                                <div className="options-container">
                                    {q.options.map((option, i) => (
                                        <div key={i} className="option-item">
                                            <input
                                                className="form-check-input custom-radio"
                                                type="radio"
                                                name={`question_${index}`}
                                                value={option}
                                                onChange={() => handleAnswerChange(index, option)}
                                            />
                                            <label
                                                className="form-check-label option-label"
                                                htmlFor={`question_${index}_${i}`}
                                            >
                                                {option}
                                            </label>
                                        </div>
                                    ))}
                                </div>
                            </div>
                        </div>
                    ))}
                    <button type="button" className="btn btn-primary" onClick={handleSubmit}>Submit</button>
                </form>
            )}

            {/* Display Results */}
            {results && (
                <div className="mt-4">
                    <h3>Results</h3>
                    {results.map((res, idx) => (
                        <p key={idx} className={res.result === 'Correct' ? 'text-success' : 'text-danger'}>
                            {res.question} - {res.result} (Your answer: {res.user_answer}, Correct: {res.correct_answer})
                        </p>
                    ))}

                    {/* Display Total Score */}
                    <div className="mt-3">
                        <h4>
                            Total Score: {totalScore} out of {results.length}
                        </h4>
                    </div>
                </div>
            )}
        </div>
    );
};

export default QuestionDisplay;