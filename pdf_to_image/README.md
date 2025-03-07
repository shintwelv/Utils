# PDF to Image
1. Read a pdf
2. Make the pdf into separate jpeg file (name it using indexes)
3. Crop edge of the images (1% margin)
    3-1. For removing background

# Rename Images
1. Read all images in directory 
2. Sort them with alphabetical order
3. Rename them

Naming Rule is follows
1. Start with Day 7
2. Each Day has two image
3. First one should have index of 0, Second one with index of 1

For example,
Day_7_0, Day_7_1, Day_8_0, Day_8_1


```python
pip install pymupdf pillow
pip install natsort
```
