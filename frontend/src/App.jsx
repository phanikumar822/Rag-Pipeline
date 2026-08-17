import { useState } from "react";
import "./index.css";

function App() {
    const [file, setFile] = useState(null);
    const [question, setQuestion] = useState("");
    const [answer, setAnswer] = useState("");
    const [uploadMessage, setUploadMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [asking, setAsking] = useState(false);

    const uploadFile = async (selectedFile) => {
        const fileToUpload = selectedFile || file;
        if (!fileToUpload) {
            setUploadMessage("Please select a PDF file.");
            return;
        }

        try {
            setLoading(true);
            setUploadMessage("");

            const formData = new FormData();
            formData.append("file", fileToUpload);

            const response = await fetch(
                (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000") + "/upload",
                {
                    method: "POST",
                    body: formData
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Upload failed");
            }

            setUploadMessage(
                `${data.message}${data.chunks ? ` • ${data.chunks} chunks` : ""}`
            );

        } catch (error) {
            console.error(error);
            setUploadMessage("Upload failed: " + error.message);
        } finally {
            setLoading(false);
        }
    };

    const askQuestion = async () => {
        if (!question.trim()) {
            setAnswer("Please enter a question.");
            return;
        }

        try {
            setAsking(true);
            setAnswer("");

            const response = await fetch(
                (import.meta.env.VITE_API_URL || "http://127.0.0.1:8000") + "/chat",
                {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        question: question
                    })
                }
            );

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || "Request failed");
            }

            setAnswer(data.answer);

        } catch (error) {
            console.error(error);
            setAnswer("Error: " + error.message);
        } finally {
            setAsking(false);
        }
    };

    return (
        <div className="app">

            {/* NAVBAR */}
            <header className="navbar">
                <div className="brand">
                    <div className="brand-mark">R</div>

                    <div>
                        <h1>Production RAG</h1>
                        <span>Document Intelligence</span>
                    </div>
                </div>

                <div className="status">
                    <span className="status-dot"></span>
                    System Online
                </div>
            </header>


            {/* MAIN */}
            <main className="container">

                {/* HERO */}
                <section className="hero">
                    <p className="eyebrow">DOCUMENT ASSISTANT</p>

                    <h2>
                        Ask questions about
                        <br />
                        your documents.
                    </h2>

                    <p className="hero-text">
                        Upload a PDF and use your knowledge base to
                        find relevant information through natural language.
                    </p>
                </section>


                {/* CONTENT GRID */}
                <div className="workspace">

                    {/* UPLOAD CARD */}
                    <section className="card upload-card">

                        <div className="card-header">
                            <div>
                                <span className="step">01</span>
                                <h3>Upload document</h3>
                            </div>
                        </div>

                        <div className="upload-box">

                            <div className="upload-icon">
                                ↑
                            </div>

                            <h4>
                                {file ? file.name : "Choose a PDF document"}
                            </h4>

                            <p>
                                {loading
                                    ? "Uploading..."
                                    : file
                                        ? "File selected"
                                        : "PDF files up to your configured limit"}
                            </p>

                            <label className="choose-btn">
                                Choose file
                                <input
                                    type="file"
                                    accept=".pdf"
                                    onChange={(e) => {
                                        const selected = e.target.files[0];
                                        setFile(selected);
                                        if (selected) {
                                            uploadFile(selected);
                                        }
                                    }}
                                />
                            </label>

                        </div>



                        {uploadMessage && (
                            <div className="message">
                                {uploadMessage}
                            </div>
                        )}

                    </section>


                    {/* QUESTION CARD */}
                    <section className="card question-card">

                        <div className="card-header">
                            <div>
                                <span className="step">02</span>
                                <h3>Ask your document</h3>
                            </div>
                        </div>

                        <div className="question-area">

                            <textarea
                                placeholder="What would you like to know?"
                                value={question}
                                onChange={(e) =>
                                    setQuestion(e.target.value)
                                }
                            />

                            <button
                                className="primary-btn ask-btn"
                                onClick={askQuestion}
                                disabled={asking}
                            >
                                {asking ? "Thinking..." : "Ask question"}
                                <span>→</span>
                            </button>

                        </div>

                    </section>

                </div>


                {/* ANSWER */}
                <section className="answer-section">

                    <div className="answer-heading">
                        <div>
                            <span className="step">03</span>
                            <h3>Answer</h3>
                        </div>

                        {answer && (
                            <span className="answer-status">
                                Retrieved
                            </span>
                        )}
                    </div>


                    <div className="answer-box">

                        {!answer ? (
                            <div className="empty-answer">

                                <div className="empty-icon">
                                    +
                                </div>

                                <h4>Your answer will appear here</h4>

                                <p>
                                    Upload a document and ask a question
                                    to get started.
                                </p>

                            </div>
                        ) : (
                            <div className="answer-content">
                                {answer}
                            </div>
                        )}

                    </div>

                </section>

            </main>


            {/* FOOTER */}
            <footer>
                <span>Production RAG</span>
                <span>Built for document search & retrieval</span>
            </footer>

        </div>
    );
}

export default App;