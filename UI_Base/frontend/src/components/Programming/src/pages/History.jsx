import React from "react";
import { useEffect, useState } from "react";
import { fetchAllQuestions } from "../apis/api";
import QuestionList from "../components/QuestionList";

function History() {
  const [filters, setFilters] = useState({ language: "", type: "", difficulty: "" });
  const [questions, setQuestions] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const data = await fetchAllQuestions(filters);
      setQuestions(data);
    };
    fetchData();
  }, [filters]);

  return <QuestionList questions={questions} setFilters={setFilters} />;
}

export default History;
