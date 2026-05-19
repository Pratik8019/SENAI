export interface RAGSearchResult {
  content: string;
  source_file: string;
  chunk_index: number;
  relevance_score: number;
  metadata: Record<string, unknown>;
}

export interface RAGSearchResponse {
  query: string;
  results: RAGSearchResult[];
  total_results: number;
}
