"""
Advanced RAG Validation

Validates rag_extensions field in ADL v2 agent definitions.
"""

from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class ValidationError:
    """Represents a validation error."""

    field: str
    message: str
    severity: str = "error"


class AdvancedRAGValidator:
    """Validator for advanced RAG configurations."""

    VALID_SEARCH_TYPES = ["semantic", "keyword", "hybrid"]
    VALID_INDEX_TYPES = ["vector", "keyword", "hierarchical", "graph"]
    VALID_EMBEDDING_MODELS = ["openai", "huggingface", "cohere", "custom"]
    VALID_CHUNK_STRATEGIES = ["fixed_size", "semantic", "recursive", "sliding_window"]
    VALID_FUSION_METHODS = ["rrf", "weighted", "rank_fusion", "custom"]
    VALID_PIPELINE_STAGES = ["preprocessing", "retrieval", "reranking", "postprocessing"]
    VALID_RERANKING_MODELS = ["cross_encoder", "monot5", "custom"]
    VALID_CACHE_TYPES = ["memory", "redis", "memcached", "database"]

    def __init__(self):
        self.errors: List[ValidationError] = []

    def validate(self, rag_extensions: Dict[str, Any]) -> List[ValidationError]:
        """Validate RAG extensions configuration."""
        self.errors = []

        if not rag_extensions:
            return []

        self._validate_rag_hierarchy(rag_extensions)
        self._validate_hybrid_search(rag_extensions)
        self._validate_pipeline(rag_extensions)
        self._validate_reranking(rag_extensions)
        self._validate_cache(rag_extensions)

        return self.errors

    def _validate_rag_hierarchy(self, rag_extensions: Dict[str, Any]) -> None:
        """Validate rag_hierarchy field."""
        rag_hierarchy = rag_extensions.get("rag_hierarchy")

        if not rag_hierarchy:
            return

        if not isinstance(rag_hierarchy, dict):
            self.errors.append(ValidationError(
                field="rag_hierarchy",
                message="RAG hierarchy must be an object"
            ))
            return

        if "index_type" not in rag_hierarchy:
            self.errors.append(ValidationError(
                field="rag_hierarchy",
                message="RAG hierarchy must have an 'index_type' field"
            ))
            return

        index_type = rag_hierarchy["index_type"]
        if index_type not in self.VALID_INDEX_TYPES:
            self.errors.append(ValidationError(
                field="rag_hierarchy.index_type",
                message=f"Invalid index_type: {index_type}. Must be one of {self.VALID_INDEX_TYPES}"
            ))

        if index_type == "hierarchical":
            if "sub_indices" not in rag_hierarchy:
                self.errors.append(ValidationError(
                    field="rag_hierarchy",
                    message="Hierarchical index must have a 'sub_indices' field"
                ))
            elif not isinstance(rag_hierarchy["sub_indices"], list):
                self.errors.append(ValidationError(
                    field="rag_hierarchy.sub_indices",
                    message="sub_indices must be an array"
                ))
            else:
                for i, sub_index in enumerate(rag_hierarchy["sub_indices"]):
                    if not isinstance(sub_index, dict):
                        self.errors.append(ValidationError(
                            field=f"rag_hierarchy.sub_indices[{i}]",
                            message="Sub-index must be an object"
                        ))
                        continue

                    if "name" not in sub_index:
                        self.errors.append(ValidationError(
                            field=f"rag_hierarchy.sub_indices[{i}]",
                            message="Sub-index must have a 'name' field"
                        ))

                    if "index_type" not in sub_index:
                        self.errors.append(ValidationError(
                            field=f"rag_hierarchy.sub_indices[{i}]",
                            message="Sub-index must have an 'index_type' field"
                        ))

        if "embedding_model" in rag_hierarchy:
            embedding_model = rag_hierarchy["embedding_model"]
            if not isinstance(embedding_model, dict):
                self.errors.append(ValidationError(
                    field="rag_hierarchy.embedding_model",
                    message="Embedding model must be an object"
                ))
            elif "provider" not in embedding_model:
                self.errors.append(ValidationError(
                    field="rag_hierarchy.embedding_model",
                    message="Embedding model must have a 'provider' field"
                ))
            elif embedding_model["provider"] not in self.VALID_EMBEDDING_MODELS:
                self.errors.append(ValidationError(
                    field="rag_hierarchy.embedding_model.provider",
                    message=f"Invalid embedding provider: {embedding_model['provider']}. Must be one of {self.VALID_EMBEDDING_MODELS}"
                ))

    def _validate_hybrid_search(self, rag_extensions: Dict[str, Any]) -> None:
        """Validate hybrid_search field."""
        hybrid_search = rag_extensions.get("hybrid_search")

        if not hybrid_search:
            return

        if not isinstance(hybrid_search, dict):
            self.errors.append(ValidationError(
                field="hybrid_search",
                message="Hybrid search must be an object"
            ))
            return

        if "search_types" not in hybrid_search:
            self.errors.append(ValidationError(
                field="hybrid_search",
                message="Hybrid search must have a 'search_types' field"
            ))
            return

        search_types = hybrid_search["search_types"]
        if not isinstance(search_types, list):
            self.errors.append(ValidationError(
                field="hybrid_search.search_types",
                message="search_types must be an array"
            ))
        else:
            for search_type in search_types:
                if search_type not in self.VALID_SEARCH_TYPES:
                    self.errors.append(ValidationError(
                        field="hybrid_search.search_types",
                        message=f"Invalid search_type: {search_type}. Must be one of {self.VALID_SEARCH_TYPES}"
                    ))

        if "fusion_method" in hybrid_search:
            fusion_method = hybrid_search["fusion_method"]
            if fusion_method not in self.VALID_FUSION_METHODS:
                self.errors.append(ValidationError(
                    field="hybrid_search.fusion_method",
                    message=f"Invalid fusion_method: {fusion_method}. Must be one of {self.VALID_FUSION_METHODS}"
                ))

        if "weights" in hybrid_search:
            weights = hybrid_search["weights"]
            if not isinstance(weights, dict):
                self.errors.append(ValidationError(
                    field="hybrid_search.weights",
                    message="Weights must be an object"
                ))
            else:
                total_weight = sum(weights.values())
                if abs(total_weight - 1.0) > 0.01:
                    self.errors.append(ValidationError(
                        field="hybrid_search.weights",
                        message=f"Weights must sum to 1.0, got {total_weight}"
                    ))

    def _validate_pipeline(self, rag_extensions: Dict[str, Any]) -> None:
        """Validate pipeline field."""
        pipeline = rag_extensions.get("pipeline")

        if not pipeline:
            return

        if not isinstance(pipeline, list):
            self.errors.append(ValidationError(
                field="pipeline",
                message="Pipeline must be an array"
            ))
            return

        for i, stage in enumerate(pipeline):
            if not isinstance(stage, dict):
                self.errors.append(ValidationError(
                    field=f"pipeline[{i}]",
                    message="Pipeline stage must be an object"
                ))
                continue

            if "stage" not in stage:
                self.errors.append(ValidationError(
                    field=f"pipeline[{i}]",
                    message="Pipeline stage must have a 'stage' field"
                ))
                continue

            stage_name = stage["stage"]
            if stage_name not in self.VALID_PIPELINE_STAGES:
                self.errors.append(ValidationError(
                    field=f"pipeline[{i}].stage",
                    message=f"Invalid stage: {stage_name}. Must be one of {self.VALID_PIPELINE_STAGES}"
                ))

            if stage_name == "preprocessing":
                if "chunk_strategy" in stage:
                    chunk_strategy = stage["chunk_strategy"]
                    if chunk_strategy not in self.VALID_CHUNK_STRATEGIES:
                        self.errors.append(ValidationError(
                            field=f"pipeline[{i}].chunk_strategy",
                            message=f"Invalid chunk_strategy: {chunk_strategy}. Must be one of {self.VALID_CHUNK_STRATEGIES}"
                        ))

    def _validate_reranking(self, rag_extensions: Dict[str, Any]) -> None:
        """Validate reranking field."""
        reranking = rag_extensions.get("reranking")

        if not reranking:
            return

        if not isinstance(reranking, dict):
            self.errors.append(ValidationError(
                field="reranking",
                message="Reranking must be an object"
            ))
            return

        if "enabled" in reranking and reranking["enabled"]:
            if "model" not in reranking:
                self.errors.append(ValidationError(
                    field="reranking",
                    message="Enabled reranking must have a 'model' field"
                ))
            else:
                model = reranking["model"]
                if not isinstance(model, dict):
                    self.errors.append(ValidationError(
                        field="reranking.model",
                        message="Reranking model must be an object"
                    ))
                elif "type" not in model:
                    self.errors.append(ValidationError(
                        field="reranking.model",
                        message="Reranking model must have a 'type' field"
                    ))
                elif model["type"] not in self.VALID_RERANKING_MODELS:
                    self.errors.append(ValidationError(
                        field="reranking.model.type",
                        message=f"Invalid reranking model type: {model['type']}. Must be one of {self.VALID_RERANKING_MODELS}"
                    ))

            if "top_k" in reranking:
                top_k = reranking["top_k"]
                if not isinstance(top_k, int) or top_k < 1:
                    self.errors.append(ValidationError(
                        field="reranking.top_k",
                        message="top_k must be a positive integer"
                    ))

    def _validate_cache(self, rag_extensions: Dict[str, Any]) -> None:
        """Validate cache field."""
        cache = rag_extensions.get("cache")

        if not cache:
            return

        if not isinstance(cache, dict):
            self.errors.append(ValidationError(
                field="cache",
                message="Cache must be an object"
            ))
            return

        if "enabled" in cache and cache["enabled"]:
            if "type" not in cache:
                self.errors.append(ValidationError(
                    field="cache",
                    message="Enabled cache must have a 'type' field"
                ))
            elif cache["type"] not in self.VALID_CACHE_TYPES:
                self.errors.append(ValidationError(
                    field="cache.type",
                    message=f"Invalid cache type: {cache['type']}. Must be one of {self.VALID_CACHE_TYPES}"
                ))

            if "ttl_seconds" in cache:
                ttl = cache["ttl_seconds"]
                if not isinstance(ttl, int) or ttl < 0:
                    self.errors.append(ValidationError(
                        field="cache.ttl_seconds",
                        message="ttl_seconds must be a non-negative integer"
                    ))

            if "max_size" in cache:
                max_size = cache["max_size"]
                if not isinstance(max_size, int) or max_size < 1:
                    self.errors.append(ValidationError(
                        field="cache.max_size",
                        message="max_size must be a positive integer"
                    ))


def validate_rag_extensions(rag_extensions: Dict[str, Any]) -> List[ValidationError]:
    """Validate RAG extensions configuration."""
    validator = AdvancedRAGValidator()
    return validator.validate(rag_extensions)
