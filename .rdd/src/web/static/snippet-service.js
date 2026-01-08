// Snippet Service - Manages prompt snippet data and operations

class SnippetService {
    constructor() {
        this.snippets = [];
        this.snippetsLoaded = false;
        this.sessionToken = null;
    }

    /**
     * Initialize the service with session token
     * @param {string} token - Session token for API calls
     */
    init(token) {
        this.sessionToken = token;
    }

    /**
     * Load snippets from the API
     * @returns {Promise<Array>} Array of snippet objects
     */
    async loadSnippets() {
        if (this.snippetsLoaded && this.snippets.length > 0) {
            return this.snippets;
        }

        try {
            const response = await fetch('/api/snippets');
            const data = await response.json();

            if (data.success) {
                this.snippets = data.snippets || [];
                this.snippetsLoaded = true;
                return this.snippets;
            } else {
                console.error('Failed to load snippets:', data.error);
                throw new Error(data.error || 'Failed to load snippets');
            }
        } catch (error) {
            console.error('Error loading snippets:', error);
            throw error;
        }
    }

    /**
     * Search snippets by key or description
     * @param {string} query - Search query
     * @returns {Array} Filtered snippets
     */
    searchSnippets(query) {
        if (!query || query.trim() === '') {
            return this.snippets;
        }

        const lowerQuery = query.toLowerCase();
        return this.snippets.filter(snippet => {
            const key = snippet.key.toLowerCase();
            const description = (snippet.description || '').toLowerCase();
            return key.includes(lowerQuery) || description.includes(lowerQuery);
        });
    }

    /**
     * Get a single snippet by exact key match
     * @param {string} key - Snippet key (e.g., "[[[ROLE_SOLUTION_ARCHITECT]]]")
     * @returns {Object|null} Snippet object or null if not found
     */
    getSnippetByKey(key) {
        return this.snippets.find(snippet => snippet.key === key) || null;
    }

    /**
     * Validate snippet keys in text
     * Finds all snippet-like patterns [[[...]]] and checks if they're valid
     * @param {string} text - Text to validate
     * @returns {Array} Array of invalid snippet keys found
     */
    validateSnippetKeys(text) {
        if (!text) {
            return [];
        }

        // Find all snippet key patterns [[[...]]]
        const pattern = /\[\[\[([^\]]+)\]\]\]/g;
        const matches = text.matchAll(pattern);
        const invalidKeys = [];
        const validKeys = new Set(this.snippets.map(s => s.key));

        for (const match of matches) {
            const fullKey = match[0]; // Full match like "[[[ROLE_SOLUTION_ARCHITECT]]]"
            if (!validKeys.has(fullKey)) {
                if (!invalidKeys.includes(fullKey)) {
                    invalidKeys.push(fullKey);
                }
            }
        }

        return invalidKeys;
    }

    /**
     * Get all available snippet keys
     * @returns {Array<string>} Array of snippet keys
     */
    getAllKeys() {
        return this.snippets.map(s => s.key);
    }

    /**
     * Refresh snippets from server (clears cache)
     * @returns {Promise<Array>} Fresh array of snippet objects
     */
    async refresh() {
        this.snippetsLoaded = false;
        this.snippets = [];
        return await this.loadSnippets();
    }
}

// Create global instance
const snippetService = new SnippetService();
