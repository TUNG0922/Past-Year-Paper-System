<template>
  <div class="lecturer-dashboard">
    <nav class="navbar">
      <img src="@/assets/upmlogo.jpg" alt="UPM Logo" class="logo" />
      <h1>UPM Lecturer Dashboard</h1>
      <div class="nav-links">
        <button @click="logout">Logout</button>
      </div>
    </nav>

    <div class="content">
      <h2>Past Year Papers</h2>
      
      <!-- Search Bar with Button -->
      <div class="search-container">
        <input
          type="text"
          v-model="searchQuery"
          placeholder="Search by Course Code..."
          class="search-input"
        />
        <button @click="filterPapers" class="search-button">Search</button>
      </div>

      <div class="papers-container">
        <div v-if="showForm" class="create-form">
          <h3>{{ isUpdate ? 'Update Past Year Paper' : 'Create Past Year Paper' }}</h3>
          <form @submit.prevent="isUpdate ? handleUpdate() : handleCreate()">
            <div>
              <label for="title">Course Code:</label>
              <input type="text" id="title" v-model="form.title" required />
            </div>
            <div>
              <label for="file">Upload File:</label>
              <input type="file" id="file" @change="handleFileUpload" required />
            </div>
            <div>
              <label for="type">Type:</label>
              <select id="type" v-model="form.type" required>
                <option value="Question">Question</option>
                <option value="Answer">Answer</option>
              </select>
            </div>
            <button type="submit">{{ isUpdate ? 'Update' : 'Submit' }}</button>
            <button type="button" @click="resetForm">Cancel</button>
          </form>
        </div>

        <table class="papers-table" v-if="!showForm">
          <thead>
            <tr>
              <th>No.</th>
              <th>Course Code</th>
              <th>Type</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(paper, index) in filteredPapers" :key="paper._id">
              <td>{{ index + 1 }}</td>
              <td>{{ paper.title }}</td>
              <td>{{ paper.type }}</td>
              <td>
                <button @click="viewPaper(paper)" class="action-button">View</button>
                <button @click="prepareUpdate(paper)" class="action-button">Update</button>
                <button @click="deletePaper(paper._id)" class="action-button delete-button">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>

        <div class="button-container" v-if="!showForm">
          <button class="create-button" @click="showForm = true">
            Create
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LecturerDashboard',
  data() {
    return {
      showForm: false,
      isUpdate: false,
      searchQuery: '', // To store the search input
      form: {
        title: '',
        file: null,
        type: 'Question',
        _id: null, // Include _id to identify the paper being updated
      },
      papers: [],
      filteredPapers: [], // Store the filtered papers
    };
  },
  async mounted() {
    await this.fetchPapers();
  },
  methods: {
    async fetchPapers() {
      try {
        const response = await fetch('http://localhost:5000/api/papers');
        if (!response.ok) {
          throw new Error('Failed to fetch papers');
        }
        const data = await response.json();
        this.papers = data.map(paper => ({
          ...paper,
          _id: paper._id.toString(),
        }));
        this.filteredPapers = this.papers; // Initialize with all papers
      } catch (error) {
        console.error('Error fetching papers:', error);
        alert('Could not fetch papers. Please try again later.');
      }
    },
    filterPapers() {
      const query = this.searchQuery.trim().toLowerCase(); // Get the trimmed search input and convert to lowercase
      if (query) {
        // Filter papers based on the exact match of the course code (case-insensitive)
        this.filteredPapers = this.papers.filter(paper => paper.title.toLowerCase() === query);
      } else {
        // If the search query is empty, show all papers
        this.filteredPapers = this.papers;
      }
    },
    async viewPaper(paper) {
      try {
        const response = await fetch(`http://localhost:5000/api/papers/${paper._id}`);
        if (!response.ok) {
          throw new Error('Failed to fetch paper');
        }
        const data = await response.json();
        window.open(`http://localhost:5000/uploads/${data.file_path.split('/').pop()}`, '_blank');
      } catch (error) {
        console.error('Error fetching paper:', error);
        alert('Could not fetch paper. Please try again later.');
      }
    },
    logout() {
      alert('Logging out...');
      this.$emit('switch-view');
    },
    handleFileUpload(event) {
      this.form.file = event.target.files[0];
    },
    async handleCreate() {
      const formData = new FormData();
      formData.append('title', this.form.title);
      formData.append('file', this.form.file);
      formData.append('type', this.form.type);

      try {
        const response = await fetch('http://localhost:5000/api/papers', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error: ${errorText}`);
        }

        const result = await response.json();
        alert('Past Year Paper created successfully!');

        this.papers.push({ 
          title: this.form.title, 
          type: this.form.type, 
          _id: result.id 
        });

        this.resetForm();
        this.filterPapers(); // Update the filtered papers
      } catch (error) {
        console.error('Error:', error);
        alert(`There was an error creating the past year paper: ${error.message}`);
      }
    },
    async handleUpdate() {
      const formData = new FormData();

      // Append only the fields that are present
      if (this.form.title) formData.append('title', this.form.title);
      if (this.form.file) formData.append('file', this.form.file);
      if (this.form.type) formData.append('type', this.form.type);

      try {
        const response = await fetch(`http://localhost:5000/api/papers/${this.form._id}`, {
          method: 'PUT',
          body: formData,
        });

        if (!response.ok) {
          const errorText = await response.text();
          throw new Error(`Error: ${errorText}`);
        }

        const updatedPaper = await response.json();
        const index = this.papers.findIndex(paper => paper._id === this.form._id);
        if (index !== -1) {
          this.papers.splice(index, 1, updatedPaper); // Update the paper in the list
        }

        alert('Past Year Paper updated successfully!');
        this.resetForm();
        this.filterPapers(); // Update the filtered papers
      } catch (error) {
        console.error('Error:', error);
        alert(`There was an error updating the past year paper: ${error.message}`);
      }
    },
    prepareUpdate(paper) {
      this.form.title = paper.title;
      this.form.type = paper.type;
      this.form._id = paper._id; // Store the ID for the update
      this.showForm = true; // Show the form to edit
      this.isUpdate = true; // Set to true for update mode
    },
    async deletePaper(paperId) {
      if (confirm('Are you sure you want to delete this paper?')) {
        try {
          const response = await fetch(`http://localhost:5000/api/papers/${paperId}`, {
            method: 'DELETE',
          });

          if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Error: ${errorText}`);
          }

          this.papers = this.papers.filter(paper => paper._id !== paperId);
          alert('Past Year Paper deleted successfully!');
          this.filterPapers(); // Update the filtered papers
        } catch (error) {
          console.error('Error:', error);
          alert(`There was an error deleting the past year paper: ${error.message}`);
        }
      }
    },
    resetForm() {
      this.showForm = false;
      this.isUpdate = false;
      this.form = { title: '', file: null, type: 'Question', _id: null }; // Reset the form
      this.searchQuery = ''; // Clear the search input
      this.filteredPapers = this.papers; // Reset the filtered papers to show all
    },
  },
};
</script>

<style scoped>
.lecturer-dashboard {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.navbar {
  background-color: rgba(0, 123, 255, 0.9);
  color: white;
  padding: 1rem;
  display: flex;
  align-items: center;
}

.logo {
  width: 50px;
  height: auto;
  margin-right: 1rem;
}

.navbar h1 {
  margin: 0;
  flex-grow: 1;
  font-size: 1.5rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.navbar button {
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.navbar button:hover {
  background-color: #cc0000;
}

.content {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  flex-grow: 1;
  text-align: center;
}

.search-container {
  margin-bottom: 1rem;
  display: flex; /* Use flex to align items */
  align-items: center; /* Center items vertically */
}

.search-input {
  padding: 0.5rem;
  width: 100%;
  max-width: 300px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.search-button {
  padding: 0.5rem 1rem;
  border-radius: 5px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  margin-left: 0.5rem; /* Space between the input and button */
  transition: background-color 0.3s;
}

.search-button:hover {
  background-color: #0056b3;
}

.papers-container {
  width: 100%;
  max-width: 800px;
  margin-top: 2rem;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  padding: 1rem;
}

.papers-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1rem;
}

.papers-table th,
.papers-table td {
  border: 1px solid #ccc;
  padding: 0.8rem;
  text-align: left;
}

.papers-table th {
  background-color: #007bff;
  color: white;
}

.papers-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.action-button {
  background-color: #007bff;
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  cursor: pointer;
  margin-right: 0.5rem;
  transition: background-color 0.3s;
}

.action-button:hover {
  background-color: #0056b3;
}

.delete-button {
  background-color: #ff4d4d;
}

.delete-button:hover {
  background-color: #cc0000;
}

.create-button {
  margin-top: 1rem;
  padding: 0.5rem 1rem;
  border-radius: 5px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

.create-button:hover {
  background-color: #0056b3;
}

.create-form {
  position: relative;
  padding: 1rem;
  background-color: rgba(255, 255, 255, 0.9);
  border-radius: 10px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  margin-bottom: 1rem;
}

.create-form h3 {
  margin-bottom: 1rem;
}

.create-form div {
  margin-bottom: 1rem;
}

.content h2 {
  margin-top: 1rem;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-top: 1rem;
}
</style>
