import React, { useState } from "react";

interface GenerationResponse {
  post: string;
}

const PostGenerator: React.FC = () => {
  // State for form inputs
  const [objective, setObjective] = useState("");
  const [tone, setTone] = useState("friendly");
  const [hashtags, setHashtags] = useState("");
  const [context, setContext] = useState("");
  const [applyEnhancements, setApplyEnhancements] = useState(true);
  const [formality, setFormality] = useState("casual");

  // State for API call status and result
  const [isLoading, setIsLoading] = useState(false);
  const [generatedPost, setGeneratedPost] = useState("");

  const handleGenerate = async () => {
    setIsLoading(true);
    setGeneratedPost(""); // clear previous result
    try {
      const response = await fetch("http://127.0.0.1:8000/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          objective,
          tone,
          hashtags,
          context,
          apply_danish_enhancements: applyEnhancements,
          formality,
        }),
      });
      const data: GenerationResponse = await response.json();
      setGeneratedPost(data.post);
    } catch (error) {
      console.error("Error generating post:", error);
      setGeneratedPost("Error generating post. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", maxWidth: "600px", margin: "0 auto" }}>
      <h1>Danish Social Media Post Generator</h1>
      <p>Create engaging posts for Instagram and Facebook</p>

      <div>
        <label>
          <strong>What's the main message or theme of your post?</strong>
        </label>
        <input
          type="text"
          value={objective}
          onChange={(e) => setObjective(e.target.value)}
          style={{ width: "100%", marginBottom: "10px" }}
        />
      </div>

      <div>
        <label>
          <strong>Select the tone for your post:</strong>
        </label>
        <div>
          {["friendly", "professional", "humorous", "custom"].map((t) => (
            <label key={t} style={{ marginRight: "10px" }}>
              <input
                type="radio"
                name="tone"
                value={t}
                checked={tone === t}
                onChange={(e) => setTone(e.target.value)}
              />
              {t.charAt(0).toUpperCase() + t.slice(1)}
            </label>
          ))}
        </div>
      </div>

      <div style={{ marginTop: "10px" }}>
        <label>
          <strong>Hashtags / Mentions:</strong>
        </label>
        <input
          type="text"
          value={hashtags}
          onChange={(e) => setHashtags(e.target.value)}
          style={{ width: "100%", marginBottom: "10px" }}
        />
      </div>

      <div>
        <label>
          <strong>Additional Context (optional):</strong>
        </label>
        <textarea
          value={context}
          onChange={(e) => setContext(e.target.value)}
          style={{ width: "100%", marginBottom: "10px" }}
        />
      </div>

      <div>
        <label>
          <strong>Apply Danish cultural enhancements:</strong>
        </label>
        <input
          type="checkbox"
          checked={applyEnhancements}
          onChange={(e) => setApplyEnhancements(e.target.checked)}
        />
      </div>

      <div style={{ marginTop: "10px" }}>
        <label>
          <strong>Formality Level:</strong>
        </label>
        <select
          value={formality}
          onChange={(e) => setFormality(e.target.value)}
          style={{ marginLeft: "10px" }}
        >
          <option value="casual">Casual</option>
          <option value="formal">Formal</option>
        </select>
      </div>

      <div style={{ marginTop: "20px" }}>
        <button onClick={handleGenerate}>Generate Post</button>
      </div>

      <div style={{ marginTop: "20px" }}>
        {isLoading ? (
          <div>
            <p>Generating...</p>
            <div style={{ width: "100%", backgroundColor: "#ddd" }}>
              <div
                style={{
                  width: "50%",
                  height: "10px",
                  backgroundColor: "#4caf50",
                  animation: "progress 2s linear infinite",
                }}
              />
            </div>
          </div>
        ) : generatedPost ? (
          <div>
            <h3>Generated Post Preview:</h3>
            <textarea
              value={generatedPost}
              onChange={(e) => setGeneratedPost(e.target.value)}
              style={{ width: "100%", height: "150px" }}
            />
            <div>
              <button onClick={handleGenerate} style={{ marginTop: "10px" }}>
                Regenerate
              </button>
            </div>
          </div>
        ) : null}
      </div>
    </div>
  );
};

export default PostGenerator;
