import matplotlib.pyplot as plt

# Sample data
x = [1, 2, 3, 4, 5]
y = [10, 20, 15, 25, 30]

# Create a plot
plt.plot(x, y, marker='o', linestyle='-', color='b', label="Sales")

# Labels and title
plt.xlabel("Days")
plt.ylabel("Revenue ($)")
plt.title("Sales Over Time")
plt.legend()

# Show the plot
plt.show()
