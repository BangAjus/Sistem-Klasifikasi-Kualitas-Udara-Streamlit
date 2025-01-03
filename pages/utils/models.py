from collections import Counter
import numpy as np

class KNN:
    
    def __init__(self, k=3, distance_metric='euclidean', p=2):
        self.k = k
        self.distance_metric = distance_metric
        self.p = p  # Used for Minkowski distance

    def fit(self, X, y):
        """Fit the model using training data."""
        self.X_train = X
        self.y_train = y

    def predict(self, X):
        """Predict the class labels for the provided data."""
        predictions = [self._predict(x) for x in X]
        return np.array(predictions)

    def _predict(self, x):
        """Predict the class label for a single instance."""
        # Compute distances between x and all training samples
        distances = self._compute_distances(x)
        
        # Get the indices of the k nearest neighbors
        k_indices = np.argsort(distances)[:self.k]
        
        # Extract the labels of the k nearest neighbors
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        
        # Return the most common class label
        most_common = Counter(k_nearest_labels).most_common(1)
        return most_common[0][0]

    def _compute_distances(self, x):
        """Compute distances from x to all training samples."""
        if self.distance_metric == 'euclidean':
            return np.sqrt(np.sum((self.X_train - x) ** 2, axis=1))
        
        elif self.distance_metric == 'manhattan':
            return np.sum(np.abs(self.X_train - x), axis=1)
        
        elif self.distance_metric == 'minkowski':
            return np.power(np.sum(np.abs(self.X_train - x) ** self.p, axis=1), 1/self.p)
        
        else:
            raise ValueError("Invalid distance metric. Choose 'euclidean', 'manhattan', or 'minkowski'.")
        
class GaussianNaiveBayes:
    
    def fit(self, X, y):
        # Separate the data by class
        self.classes = np.unique(y)
        self.means = {}  # Mean of each feature per class
        self.variances = {}  # Variance of each feature per class
        self.priors = {}  # Prior probabilities of each class
        
        # Calculate the mean, variance, and prior for each class
        for cls in self.classes:
            X_cls = X[y == cls]
            self.means[cls] = np.mean(X_cls, axis=0)
            self.variances[cls] = np.var(X_cls, axis=0)
            self.priors[cls] = X_cls.shape[0] / X.shape[0]
    
    def gaussian_probability(self, x, mean, var):
        # Calculate the Gaussian probability density function
        eps = 1e-6  # To prevent division by zero
        coeff = 1.0 / np.sqrt(2.0 * np.pi * (var + eps))
        exponent = np.exp(- (x - mean) ** 2 / (2 * (var + eps)))
        return coeff * exponent
    
    def predict(self, X):
        predictions = []
        for x in X:
            # Calculate the posterior probability for each class
            posteriors = {}
            for cls in self.classes:
                
                conditional = np.prod(self.gaussian_probability(x, self.means[cls], self.variances[cls]))
                posteriors[cls] = self.priors[cls] * conditional
            
            # Select the class with the highest posterior probability
            predictions.append(max(posteriors, key=posteriors.get))
        return np.array(predictions)
   