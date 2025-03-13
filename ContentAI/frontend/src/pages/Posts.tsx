import React, { useEffect, useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import { StoredPost } from '../types';
import { getPostHistory, deletePost } from '../services/api';

const Posts: React.FC = () => {
  const [posts, setPosts] = useState<StoredPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();

  const fetchPosts = async () => {
    try {
      const fetchedPosts = await getPostHistory();
      setPosts(fetchedPosts);
    } catch (error) {
      console.error('Failed to fetch posts:', error);
      setError('Failed to load posts. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) {
      fetchPosts();
    } else {
      setLoading(false);
    }
  }, [user]);

  const handleDelete = async (postId: string) => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      try {
        await deletePost(postId);
        setPosts(posts.filter(post => post._id !== postId));
      } catch (err) {
        console.error('Failed to delete post:', err);
        setError('Failed to delete post. Please try again.');
      }
    }
  };

  const handleCopy = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      alert('Post copied to clipboard!');
    } catch (err) {
      console.error('Failed to copy post:', err);
      setError('Failed to copy post. Please try again.');
    }
  };

  if (loading) {
    return <div>Loading posts...</div>;
  }

  if (!user) {
    return (
      <div className="page-container">
        <div className="login-prompt">
          <h2>Login Required</h2>
          <p>Please login to see your saved posts</p>
          <Link to="/login">Go to Login</Link>
        </div>
      </div>
    );
  }

  return (
    <div className="page-container">
      <h2 className="page-title">Your Saved Posts</h2>
      {error && (
        <div className="error-message">
          {error}
        </div>
      )}
      <div className="posts-grid">
        {posts.map((post) => (
          <div key={post._id} className="post-card">
            <div className="post-header">
              <span className="post-template">{post.template}</span>
              <span className="post-date">
                {new Date(post.created_at).toLocaleDateString()}
              </span>
            </div>
            <div className="post-objective">{post.objective}</div>
            <div className="post-content">{post.generated_content}</div>
            <div className="post-actions">
              <button 
                onClick={() => handleCopy(post.generated_content)}
              >
                Copy
              </button>
              <button 
                onClick={() => handleDelete(post._id)}
              >
                Delete
              </button>
            </div>
          </div>
        ))}
        {posts.length === 0 && (
          <div className="no-posts">
            <p>You haven't saved any posts yet.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Posts;
