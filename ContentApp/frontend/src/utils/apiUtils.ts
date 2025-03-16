type ApiOperation<T> = () => Promise<T>;

interface ApiErrorOptions {
  context: string;
  onError?: (error: Error) => void;
}

export async function withErrorHandling<T>(
  operation: ApiOperation<T>,
  { context, onError }: ApiErrorOptions
): Promise<T | null> {
  try {
    return await operation();
  } catch (error) {
    const errorMessage = error instanceof Error ? error.message : "An unknown error occurred";
    const enhancedError = new Error(
      `${context} failed: ${errorMessage}${
        errorMessage.toLowerCase().includes("http error")
          ? " Please ensure the backend server is running and configured properly."
          : ""
      }`
    );
    
    if (onError) {
      onError(enhancedError);
    }
    
    return null;
  }
}
