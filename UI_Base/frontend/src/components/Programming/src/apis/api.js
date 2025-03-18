import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:8000/api/v1/programming/1";

export const fetchQuestion = async (data) => {
  try {
    const response = await axios.post(`${API_BASE_URL}/generators/`, data);
    return response.data;
  } catch (error) {
    console.error("Error fetching question:", error);
    throw error;
  }
};

export const fetchAllQuestions = async (filters) => {
  try {
    const response = await axios.get(`${API_BASE_URL}/questions`, { params: filters });
    return response.data;
  } catch (error) {
    console.error("Error fetching questions:", error);
    throw error;
  }
};
