import React, { useState, ChangeEvent } from "react";
import { TemplateType, GenerationType } from "../types";
import { GenerationRequest } from "../types";
import { TEMPLATES } from "../constants";
import { generatePost, savePost, generateImage } from "../services/api";
import { useAuth } from "../contexts/AuthContext"; // added

const PostGenerator: React.FC = () => {
  const [formData, setFormData] = useState<GenerationRequest>({
    template: "tech-insight",
    objective: "",
    context: "",
    documents: [],
    type: "text", // Added the required 'type' property
  });
  const [isLoading, setIsLoading] = useState(false);
  const [generatedPost, setGeneratedPost] = useState("");
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth(); // added
  const [generationType, setGenerationType] = useState<GenerationType>("text");
  const [generatedImage, setGeneratedImage] = useState<string | null>(null);

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

  const handleError = (error: unknown, context: string) => {
    console.error(`Error ${context}:`, error);
    let errorMsg = "";
    if (error instanceof Error) {
      errorMsg = error.message;
    } else {
      errorMsg = "An unknown error occurred.";
    }
    
    // Enhance error with hints based on common issues
    if (errorMsg.toLowerCase().includes("http error")) {
      errorMsg += " Please ensure the backend server is running and configured properly.";
    }
    if (errorMsg.toLowerCase().includes("not found")) {
      errorMsg += " Please verify the API endpoint.";
    }
    
    setError(`${context} failed: ${errorMsg}`);
  };

  const handleImageGenerate = async (): Promise<string | null> => {
    try {
      setError(null);
      const response = await generateImage({
        ...formData,
        type: 'image'
      });
      console.log("Image generation response:", response); // Debug log
      if (response && response.image_url) {
        await new Promise((resolve, reject) => {
          const img = new Image();
          img.onload = () => {
            setGeneratedImage(response.image_url);
            resolve(null);
          };
          img.onerror = () => {
            reject(new Error('Failed to load image'));
          };
          img.src = response.image_url;
        });
        return response.image_url;
      } else if (response && response.error) {
        throw new Error(response.error);
      }
      throw new Error('Invalid image generation response: ' + JSON.stringify(response));
    } catch (error) {
      handleError(error, "Image generation");
      return null;
    }
  };

  const handleTextGenerate = async (): Promise<string | null> => {
    try {
      console.log('Starting post generation with data:', formData);
      const response = await generatePost({
        ...formData,
        type: generationType
      });
      console.log('Generation successful:', response);
      if ('post' in response) {
        setGeneratedPost(response.post);
        return response.post;
      }
      throw new Error('Invalid text generation response');
    } catch (error) {
      handleError(error, "Post generation");
      return null;
    }
  };

  const handleGenerate = async () => {
    if (!formData.objective || !formData.context) {
      setError("Please fill in all required fields");
      return;
    }

    setIsLoading(true);
    setError(null);

    try {
      // Clear previous content when switching types
      if (generationType !== "full") {
        setGeneratedPost("");
        setGeneratedImage(null);
      }

      switch (generationType) {
        case "text":
          await handleTextGenerate();
          break;
        case "image":
          await handleImageGenerate();
          break;
        case "full":
          const [imageUrl, postText] = await Promise.all([
            handleImageGenerate(),
            handleTextGenerate()
          ]);
          if (!imageUrl && !postText) {
            setError("Failed to generate both image and text");
          }
          break;
      }
    } finally {
      setIsLoading(false);
    }
  };

  const handleSave = async () => {
    try {
      if (generationType === "image" && generatedImage) {
        await savePost({
          template: formData.template,
          objective: formData.objective,
          context: formData.context,
          generated_content: generatedImage,
          type: "image"
        });
      } else if (generatedPost) {
        await savePost({
          template: formData.template,
          objective: formData.objective,
          context: formData.context,
          generated_content: generatedPost,
          type: generationType === "full" ? "full" : "text"
        });
      }
      alert("Content saved successfully");
    } catch (err) {
      handleError(err, "Saving content");
    }
  };

  const renderGenerationOptions = () => (
    <div className="generation-type-buttons">
      <button
        className={`generation-type-button ${generationType === 'text' ? 'active' : ''}`}
        onClick={() => {
          setGenerationType('text');
          handleGenerate();
        }}
        disabled={isLoading || !formData.objective || !formData.context}
      >
        {isLoading && generationType === 'text' ? 'Generating...' : 'Generate Text'}
      </button>
      <button
        className={`generation-type-button ${generationType === 'image' ? 'active' : ''}`}
        onClick={() => {
          setGenerationType('image');
          handleGenerate();
        }}
        disabled={isLoading || !formData.objective || !formData.context}
      >
        {isLoading && generationType === 'image' ? 'Generating...' : 'Generate Image'}
      </button>
      <button
        className={`generation-type-button ${generationType === 'full' ? 'active' : ''}`}
        onClick={() => {
          setGenerationType('full');
          handleGenerate();
        }}
        disabled={isLoading || !formData.objective || !formData.context}
      >
        {isLoading && generationType === 'full' ? 'Generating...' : 'Generate Full Post'}
      </button>
    </div>
  );

  return (
    <div className="post-generator-container">
      <div className="post-generator-input">
        <div className="form-group">
          <label><strong>Select Template</strong></label>
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
          <label><strong>Supporting Documents</strong></label>
          <div className="file-upload">
            <div className="file-input-wrapper">
              <div className="custom-file-button">Choose Files</div>
              <input type="file" multiple onChange={handleFileUpload} accept=".pdf,.doc,.docx,.txt" />
            </div>
            <p className="file-help">Upload relevant documents (PDF, DOC, TXT)</p>
          </div>
        </div>

        <div className="form-group">
          {renderGenerationOptions()}
        </div>
      </div>

      <div className="post-generator-preview">
        <div className="preview-content">
          <h3>Preview</h3>
          {isLoading && (
            <div className="preview-loading-overlay">
              <p>Creating your {generationType === 'image' ? 'visual' : 'post'}...</p>
              <div className="progress-bar">
                <div className="progress-bar-fill" />
              </div>
            </div>
          )}

          {/* Image Preview Section */}
          {(generationType === 'image' || generationType === 'full') && generatedImage && (
            <div className="image-preview">
              <img src={generatedImage} alt="Generated post visual" className="generated-image" />
              {generationType === 'image' && (
                <div className="action-buttons">
                  <button onClick={() => window.open(generatedImage, '_blank')}>View Full Size</button>
                  {user && <button onClick={handleSave}>Save Image</button>}
                </div>
              )}
            </div>
          )}

          {/* Text Preview Section */}
          {(generationType === 'text' || generationType === 'full') && (
            generatedPost ? (
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
                  {user && <button onClick={handleSave}>Save Post</button>}
                </div>
              </>
            ) : (!generatedImage && (
              <div className="empty-preview">
                <p>Generate content to see the preview here</p>
              </div>
            ))
          )}
        </div>
      </div>
    </div>
  );
};

export default PostGenerator;
