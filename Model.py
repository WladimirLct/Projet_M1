from transformers import AutoImageProcessor, ResNetForImageClassification
from transformers import ViTImageProcessor, ViTForImageClassification
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import torch
from torch import nn, optim
torch.cuda.empty_cache() # Clear cache
torch.cuda.reset_max_memory_allocated()  # Reset the max memory allocated counter
torch.cuda.reset_accumulated_memory_stats()  # Reset the accumulated memory stats
def config_vit_base():
    global transform, processor, model, model_name

    # Define the transformations
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])

    # Initialize the processor and model
    processor = ViTImageProcessor.from_pretrained('google/vit-base-patch16-224')
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224')

    num_ftrs = model.classifier.in_features  # Get the number of in_features from the current layer

    model_name = "google-vit-base-patch16-224"

    model.classifier = nn.Linear(num_ftrs, 2)  # Replace with a new Linear layer with 2 outputs
# Configure the model
config_vit_base()

# Check what layers are trainable
# for name, param in model.named_parameters():
#     print(name, param.requires_grad)

print(model.classifier)

# Specify the number of epochs
num_epochs = 30
batch_size = 30
learning_rate = 0.0001
dataset_path = "./DataClassification/Split_dataset/"
train_dataset = datasets.ImageFolder(root=dataset_path + 'Train', transform=transform)
val_dataset = datasets.ImageFolder(root=dataset_path + 'Valid', transform=transform)
test_dataset = datasets.ImageFolder(root=dataset_path + 'Test', transform=transform)

# Data loaders
train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)
print(f"Train batches: {len(train_loader)}, Validation batches: {len(val_loader)}, Test batches: {len(test_loader)}")
def get_device():
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")
# Loss function and optimizer
loss_function = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=learning_rate)

# Check for GPU availability
device = get_device()
print(f"Using device: {device}")

# Transfer the model to GPU
model = model.to(device)

# Training and validation loop
for epoch in range(num_epochs):
    # Training
    model.train()
    total_loss = 0
    train_total = 0
    train_correct = 0

    for batch_idx, (images, labels) in enumerate(train_loader):
        # Transfer images and labels to GPU
        images, labels = images.to(device), labels.to(device)

        # Forward pass
        outputs = model(images).logits

        # Compute loss
        loss = loss_function(outputs, labels)
        total_loss += loss.item()

        # Compute accuracy
        _, predicted = torch.max(outputs.data, 1)
        train_total += labels.size(0)
        train_correct += (predicted == labels).sum().item()

        # Backward pass and optimization
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        if (batch_idx+1) % 10 == 0:
            pass
            # print(f'Epoch: {epoch+1}, Batch: {batch_idx+1}, Loss: {loss.item()}')

    # Validation
    model.eval()
    val_total_loss = 0
    val_total = 0
    val_correct = 0

    with torch.no_grad():
        for images, labels in val_loader:
            # Transfer images and labels to GPU
            images, labels = images.to(device), labels.to(device)

            # Forward pass
            outputs = model(images).logits

            # Compute loss
            val_loss = loss_function(outputs, labels)
            val_total_loss += val_loss.item()

            # Compute accuracy
            _, predicted = torch.max(outputs.data, 1)
            val_total += labels.size(0)
            val_correct += (predicted == labels).sum().item()

    # Calculate average loss and accuracy for the epoch
    avg_loss = total_loss / len(train_loader)
    train_accuracy = 100 * train_correct / train_total

    # Calculate average validation loss and accuracy
    avg_val_loss = val_total_loss / len(val_loader)
    val_accuracy = 100 * val_correct / val_total

    print(f'Epoch {epoch+1}, \tAverage Training Loss: \t{avg_loss}, \tTraining Accuracy: \t{train_accuracy}%')
    print(f'Epoch {epoch+1}, \tAverage Validation Loss: \t{avg_val_loss}, \tValidation Accuracy: \t{val_accuracy}%')

# Print the max memory allocated
print(torch.cuda.max_memory_allocated() / 1024 ** 2, 'MB')
# Testing loop
model.eval()  # Set the model to evaluation mode
test_total = 0
test_correct = 0

with torch.no_grad():  # No gradients needed for testing, saves memory and computations
    for images, labels in test_loader:
        # Transfer images and labels to GPU (if using)
        images, labels = images.to(device), labels.to(device)

        # Forward pass
        outputs = model(images).logits

        # Compute accuracy
        _, predicted = torch.max(outputs.data, 1)
        test_total += labels.size(0)    
        test_correct += (predicted == labels).sum().item()

# Print test accuracy
test_accuracy = 100 * test_correct / test_total
print(f'Test Accuracy: {test_accuracy}%')   
# Save the model
torch.save(model.state_dict(), f'{model_name}.pth')

# Print the max memory allocated
print(torch.cuda.max_memory_allocated() / 1024 ** 2, 'MB')
# Let's predict on a whole folder of images
import os
from PIL import Image
import numpy as np

device = get_device()

#! We reconfigure the model so that this cell can be run independently
config_vit_base()

# Load model from saved file to make sure we are using the model we just trained
#? Could be skipped but added for clarity
model.load_state_dict(torch.load(f'{model_name}.pth'))
model.eval()
model.to(device)

# Get the list of images
dir_list = os.listdir('./Classify')

sclerosed = []
images = []

# Get the list of images by dir
for dir in dir_list:
    image_list = os.listdir(f'./Classify/{dir}')

    i = 0
    # Loop through the images
    for image in image_list:
        images.append(image)

        # Load the image
        img = Image.open(f'./Classify/{dir}/{image}')

        # Transform the image
        img = transform(img)

        # Add a batch dimension
        img = img.unsqueeze(0)

        # Transfer the image to GPU (if using)
        img = img.to(device)

        # Forward pass
        output = model(img).logits

        # Get the predicted class
        _, predicted = torch.max(output.data, 1)

        i += 1
        if (predicted.item()):
            # Print the prediction
            print(f'Image \t{image[24:-5]} \tof {dir} is predicted to be a sclerosed glomerulus')
            sclerosed.append(image)

print(f"Total sclerosed: {len(sclerosed)}")

# Save the list of sclerosed images as csv
import csv

with open(f'./Predictions/{model_name}.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Loop through the list of images
    for image in images:
        writer.writerow([image, 1 if image in sclerosed else 0])