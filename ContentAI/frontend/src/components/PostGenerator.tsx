import React, { useState, ChangeEvent } from "react";
import { TemplateType } from "../types"; // Add this line to import TemplateType
import { GenerationRequest, GenerationResponse } from "../types";
import { TEMPLATES } from "../constants";
import { generatePost } from "../services/api";

const PostGenerator: React.FC = () => {
  const [formData, setFormData] = useState<GenerationRequest>({
    template: "tech-insight",
    objective: "",
    context: "",
    documents: [],
  });
  const [isLoading, setIsLoading] = useState(false);
  const [generatedPost, setGeneratedPost] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleTemplateSelect = (templateId: TemplateType) => {
    setFormData(prev => ({
      ...prev,
      template: templateId
    }));
  };

  const handleInputChange = (e: ChangeEvent<HTMLTextAreaElement | HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFormData({ ...formData, documents: Array.from(e.target.files) });
    }
  };

  const handleGenerate = async () => {
    setIsLoading(true);
    setGeneratedPost("");
    setError(null);

    try {
      const response = await generatePost(formData);
      setGeneratedPost(response.post);
    } catch (error) {
      console.error("Error generating post:", error);
      setError("Failed to generate post. Please try again.");
      setGeneratedPost("");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="post-generator-container">
      <div className="post-generator-input">
        <h2>Create Engaging LinkedIn Posts</h2>
        
        <div className="form-group">
          <label>
            <strong>Select Template</strong>
          </label>
          <div className="template-buttons">
            {TEMPLATES.map(template => (
              <button
                key={template.id}
                className={`template-button ${formData.template === template.id ? 'active' : ''}`}
                onClick={() => handleTemplateSelect(template.id)}
                type="button"
              >
                <div className="template-button-content">
                  <strong>{template.label}</strong>
                  <small>{template.description}</small>
                </div>
              </button>
            ))}
          </div>
        </div>

        <div className="form-group">
          <label>
            <strong>Main Message or Theme</strong>
            <textarea
              name="objective"
              value={formData.objective}
              onChange={handleInputChange}
              placeholder="Describe the main message or theme of your post..."
              rows={3}
            />
          </label>
        </div>

        <div className="form-group">
          <label>
            <strong>Context</strong>
            <textarea
              name="context"
              value={formData.context}
              onChange={handleInputChange}
              placeholder="Add any relevant context about your company, product, or industry..."
              rows={4}
            />
          </label>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="form-group">
          <label>
            <strong>Supporting Documents</strong>
          </label>
          <div className="file-upload">
            <div className="file-input-wrapper">
              <div className="custom-file-button">Choose Files</div>
              <input
                type="file"
                multiple
                onChange={handleFileUpload}
                accept=".pdf,.doc,.docx,.txt"
              />
            </div>
            <p className="file-help">Upload relevant documents (PDF, DOC, TXT)</p>
          </div>
        </div>

        <div className="form-group">
          <button 
            onClick={handleGenerate} 
            disabled={isLoading || !formData.objective || !formData.context}
          >
            {isLoading ? "Generating..." : "Generate Post"}
          </button>
        </div>
      </div>

      <div className="post-generator-preview">
        <div className="preview-content">
          <h3>Post Preview</h3>
          {isLoading && (
            <div className="preview-loading-overlay">
              <p>Crafting your LinkedIn post...</p>
              <div className="progress-bar">
                <div className="progress-bar-fill" />
              </div>
            </div>
          )}
          {generatedPost ? (
            <>
              <textarea
                value={generatedPost}
                onChange={(e) => setGeneratedPost(e.target.value)}
                className="generated-post"
                placeholder="Your generated post will appear here..."
                rows={15}
              />
              <div className="action-buttons">
                <button onClick={handleGenerate}>Regenerate</button>
                <button onClick={() => navigator.clipboard.writeText(generatedPost)}>
                  Copy to Clipboard
                </button>
              </div>
            </>
          ) : (
            <div className="empty-preview">
              <p>Generate a post to see the preview here</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default PostGenerator;
