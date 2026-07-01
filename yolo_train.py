from ultralytics import YOLO

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo26n.pt")

# Perform object detection on an image using the model
results = model("https://scontent.fgru6-1.fna.fbcdn.net/v/t39.30808-6/589031725_10228163192779850_9035292577819860692_n.jpg?stp=dst-jpg_tt6&cstp=mx1080x1080&ctp=p526x296&_nc_cat=107&ccb=1-7&_nc_sid=833d8c&_nc_ohc=XfsICrSYVnoQ7kNvwFEVfAg&_nc_oc=AdqTMVoZdxlpHbUxX1nsCBMH10HUUtbDDD6HwFBBFOnHgtetUc9rMn6dogO9mm15NPo&_nc_zt=23&_nc_ht=scontent.fgru6-1.fna&_nc_gid=292D0u-TKOLrTr2P3dn30g&_nc_ss=7b289&oh=00_AQBdwpamDcwHrcZSbQiFJCjO8Kndybzo5PJLWYrw9g3rTA&oe=6A4A340E")

# Visualize the results
for result in results:
    result.show()