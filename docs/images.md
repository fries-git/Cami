# Upload Image

POST /uploadimage `multipart/form-data: token=<str>, image=<file>, filename=<str>`
On Success: Returns `{"msg":"Uploaded!","filename":"<filename>.<ext>"}` with code `201`.
On Failure: Returns code `400`. (Missing/invalid token or no image uploaded.)
On Failure: Returns code `409`. (File with that name already exists.)
Supports PNG, JPEG, and other non-GIF image formats, which are converted to PNG. GIFs are preserved as animated GIFs. Images are resized so their largest dimension is at most `300px`.
  
# Get Image
GET `/getimage/<filename>`
On Success: Returns the image file with code `200`.
On Failure: Returns code `404`. (Image doesn't exist.)
Automatically checks for both `<filename>.png` and `<filename>.gif`.
  
# Get GIF
GET `/getgif/<filename>.gif`
On Success: Returns the GIF file with code `200`.
On Failure: Returns code `404`. (GIF doesn't exist.)