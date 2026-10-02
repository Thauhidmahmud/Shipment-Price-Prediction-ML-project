
from shipment.configuration.s3_operation import S3Operation


s3 = S3Operation()


# Upload
s3.upload_file(
    file_path=r"G:\Bootcamp\data\shipment.csv",
    s3_key="data/shipment.csv"
)

print("Upload successful!")


# Read CSV directly from S3
df = s3.read_csv("data/shipment.csv")

print(df.head())
print(df.shape)


# List files
files = s3.list_files()

print("\nFiles in S3:")

for file in files:
    print(file)