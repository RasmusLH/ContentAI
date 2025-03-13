import React, { useEffect, useState, useCallback } from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Link } from 'react-router-dom';
import { StoredPost } from '../types';
import { getPostHistory, deletePost } from '../services/api';
import { useNotification } from '../contexts/NotificationContext';
import LoadingSkeleton from '../components/LoadingSkeleton';

const Posts: React.FC = () => {
  const [posts, setPosts] = useState<StoredPost[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { user } = useAuth();
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [isSearching, setIsSearching] = useState(false);
  const { showNotification } = useNotification();
  const ITEMS_PER_PAGE = 6;

  const fetchPosts = useCallback(async (pageNum: number, search?: string) => {
    setLoading(true);
    setError(null);
    try {
      const response = await getPostHistory(ITEMS_PER_PAGE, (pageNum - 1) * ITEMS_PER_PAGE, search);
      if (!response.posts || !Array.isArray(response.posts)) {
        throw new Error('Invalid response format');
      }
      setPosts(response.posts);
      setTotalPages(response.totalPages);
      if (pageNum > response.totalPages && response.totalPages > 0) {
        // If current page is beyond total pages, reset to last valid page
        setPage(response.totalPages);
      }
    } catch (error) {
      const errorMessage = error instanceof Error ? error.message : 'Failed to load posts';
      setError(errorMessage);
      showNotification(errorMessage, 'error');
      setPosts([]);
      setTotalPages(1);
    } finally {
      setLoading(false);
      setIsSearching(false);
    }
  }, [showNotification]);

  useEffect(() => {
    let isMounted = true;

    const loadPosts = async () => {
      if (user && isMounted) {
        await fetchPosts(page, searchTerm);
      } else if (isMounted) {
        setLoading(false);
      }
    };

    loadPosts();

    return () => {
      isMounted = false;
    };
  }, [user, page, searchTerm, fetchPosts]);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!isSearching) {
      setIsSearching(true);
      setPage(1);
      await fetchPosts(1, searchTerm);
    }
  };

  const clearSearch = async () => {
    setSearchTerm('');
    setPage(1);
    await fetchPosts(1, '');
  };

  const handleDelete = async (postId: string) => {
    if (window.confirm('Are you sure you want to delete this post?')) {
      try {
        await deletePost(postId);
        setPosts(posts.filter(post => post._id !== postId));
        showNotification('Post deleted successfully', 'success');
      } catch (err) {
        showNotification('Failed to delete post', 'error');
      }
    }
  };

  const handleCopy = async (content: string) => {
    try {
      await navigator.clipboard.writeText(content);
      showNotification('Post copied to clipboard', 'success');
    } catch (err) {
      showNotification('Failed to copy post', 'error');
    }
  };

  const renderSkeletonLoaders = () => (
    <>
      {Array(ITEMS_PER_PAGE).fill(0).map((_, idx) => (
        <div key={idx} className="post-card">
          <div className="post-header">
            <LoadingSkeleton width="100px" height="20px" />
            <LoadingSkeleton width="80px" height="20px" />
          </div>
          <LoadingSkeleton width="100%" height="24px" className="post-objective" />
          <LoadingSkeleton count={3} className="post-content" />
        </div>
      ))}
    </>
  );

  if (loading) {
    return (
      <div className="page-container">
        <h2 className="page-title">Your Saved Posts</h2>
        <div className="posts-grid">
          {renderSkeletonLoaders()}
        </div>
      </div>
    );
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
      
      <div className="posts-controls">
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search posts..."
            className="search-input"
          />
          <button type="submit" disabled={isSearching}>
            {isSearching ? 'Searching...' : 'Search'}
          </button>
          {searchTerm && (
            <button type="button" onClick={clearSearch}>
              Clear
            </button>
          )}
        </form>
      </div>

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

      {totalPages > 1 && (
        <div className="pagination">
          <button
            onClick={() => setPage(p => Math.max(1, p - 1))}
            disabled={page === 1 || loading}
          >
            Previous
          </button>
          <span className="page-info">
            Page {page} of {totalPages}
          </span>
          <button
            onClick={() => setPage(p => Math.min(totalPages, p + 1))}
            disabled={page === totalPages || loading}
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default Posts;
