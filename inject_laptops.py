import pandas as pd

# 1. Add New CPUs
cpu_new = pd.DataFrame([
    {
        "CPU": "Core i9-13980HX", "Codename": "Raptor Lake", "Min_Cores": 24, "Max_Cores": 24, 
        "Clock": "2.2 to 5.6 GHz", "Min_Clock": 2.2, "Min_Clock(MHz)": 2200, "Max_Clock": 5.6, 
        "Max_Clock(MHz)": 5600, "Size": "GHz", "Socket": "BGA 1964", "Process": "10 nm", 
        "Process(NM)": 10, "TDP(Watts)": 55, "Release": "Jan 3rd, 2023"
    },
    {
        "CPU": "Core i7-13700HX", "Codename": "Raptor Lake", "Min_Cores": 16, "Max_Cores": 16, 
        "Clock": "2.1 to 5.0 GHz", "Min_Clock": 2.1, "Min_Clock(MHz)": 2100, "Max_Clock": 5.0, 
        "Max_Clock(MHz)": 5000, "Size": "GHz", "Socket": "BGA 1964", "Process": "10 nm", 
        "Process(NM)": 10, "TDP(Watts)": 55, "Release": "Jan 3rd, 2023"
    },
    {
        "CPU": "Ryzen 9 7940HS", "Codename": "Phoenix", "Min_Cores": 8, "Max_Cores": 8, 
        "Clock": "4.0 to 5.2 GHz", "Min_Clock": 4.0, "Min_Clock(MHz)": 4000, "Max_Clock": 5.2, 
        "Max_Clock(MHz)": 5200, "Size": "GHz", "Socket": "FP8", "Process": "4 nm", 
        "Process(NM)": 4, "TDP(Watts)": 35, "Release": "Jan 4th, 2023"
    },
    {
        "CPU": "Core i9-14900HX", "Codename": "Raptor Lake Refresh", "Min_Cores": 24, "Max_Cores": 24, 
        "Clock": "2.2 to 5.8 GHz", "Min_Clock": 2.2, "Min_Clock(MHz)": 2200, "Max_Clock": 5.8, 
        "Max_Clock(MHz)": 5800, "Size": "GHz", "Socket": "BGA 1964", "Process": "10 nm", 
        "Process(NM)": 10, "TDP(Watts)": 55, "Release": "Jan 8th, 2024"
    }
])

# 2. Add New GPUs
gpu_new = pd.DataFrame([
    {
        "manufacturer": "NVIDIA", "productName": "GeForce RTX 4090 Mobile", "GPU": "NVIDIA GeForce RTX 4090 Mobile",
        "Year_Released": 2023, "Memory (GB)": 16, "Memory(MB)": 16384, "Memory_bus(BIT)": 256,
        "Memory_Clock(MHz)": 2250, "BUS": "PCIe 4.0 x16", "Memory_Type": "GDDR6", "Chip": "AD103"
    },
    {
        "manufacturer": "NVIDIA", "productName": "GeForce RTX 4080 Mobile", "GPU": "NVIDIA GeForce RTX 4080 Mobile",
        "Year_Released": 2023, "Memory (GB)": 12, "Memory(MB)": 12288, "Memory_bus(BIT)": 192,
        "Memory_Clock(MHz)": 2250, "BUS": "PCIe 4.0 x16", "Memory_Type": "GDDR6", "Chip": "AD104"
    },
    {
        "manufacturer": "NVIDIA", "productName": "GeForce RTX 4070 Mobile", "GPU": "NVIDIA GeForce RTX 4070 Mobile",
        "Year_Released": 2023, "Memory (GB)": 8, "Memory(MB)": 8192, "Memory_bus(BIT)": 128,
        "Memory_Clock(MHz)": 2000, "BUS": "PCIe 4.0 x8", "Memory_Type": "GDDR6", "Chip": "AD106"
    }
])

# 3. Add New Laptops
laptop_new = pd.DataFrame([
    {
        "LaptopID": 2001, "Company": "Asus", "Type": "Gaming", "Inches": 18.0, "ScreenAndRes": "QHD+ 2560x1600",
        "Screen": "QHD+", "Resolution": "2560x1600", "CpuMan": "Intel", "CPU/Withclock": "Core i9-13980HX 2.2GHz",
        "CPU": "Core i9-13980HX", "Ram": "32GB", "Ram(GB)": 32, "Storage(Primary)": "2TB SSD", "Storage(Secondary)": "",
        "Storage(P(GB))": 2000, "Storage(S(GB))": 0, "Storage(GB)": "2,000", "Gpu": "NVIDIA GeForce RTX 4090 Mobile", "OS": "Windows 11"
    },
    {
        "LaptopID": 2002, "Company": "Lenovo", "Type": "Gaming", "Inches": 16.0, "ScreenAndRes": "WQXGA 2560x1600",
        "Screen": "WQXGA", "Resolution": "2560x1600", "CpuMan": "Intel", "CPU/Withclock": "Core i7-13700HX 2.1GHz",
        "CPU": "Core i7-13700HX", "Ram": "16GB", "Ram(GB)": 16, "Storage(Primary)": "1TB SSD", "Storage(Secondary)": "",
        "Storage(P(GB))": 1000, "Storage(S(GB))": 0, "Storage(GB)": "1,000", "Gpu": "NVIDIA GeForce RTX 4070 Mobile", "OS": "Windows 11"
    },
    {
        "LaptopID": 2003, "Company": "Razer", "Type": "Gaming", "Inches": 14.0, "ScreenAndRes": "QHD+ 2560x1600",
        "Screen": "QHD+", "Resolution": "2560x1600", "CpuMan": "AMD", "CPU/Withclock": "Ryzen 9 7940HS 4.0GHz",
        "CPU": "Ryzen 9 7940HS", "Ram": "16GB", "Ram(GB)": 16, "Storage(Primary)": "1TB SSD", "Storage(Secondary)": "",
        "Storage(P(GB))": 1000, "Storage(S(GB))": 0, "Storage(GB)": "1,000", "Gpu": "NVIDIA GeForce RTX 4080 Mobile", "OS": "Windows 11"
    },
    {
        "LaptopID": 2004, "Company": "Alienware", "Type": "Gaming", "Inches": 16.0, "ScreenAndRes": "QHD+ 2560x1600",
        "Screen": "QHD+", "Resolution": "2560x1600", "CpuMan": "Intel", "CPU/Withclock": "Core i9-14900HX 2.2GHz",
        "CPU": "Core i9-14900HX", "Ram": "32GB", "Ram(GB)": 32, "Storage(Primary)": "2TB SSD", "Storage(Secondary)": "",
        "Storage(P(GB))": 2000, "Storage(S(GB))": 0, "Storage(GB)": "2,000", "Gpu": "NVIDIA GeForce RTX 4090 Mobile", "OS": "Windows 11"
    }
])

print("Updating files...")

# Append to original CSVs (read, concat, write)
cpu_df = pd.read_csv("CPU_Specs.csv")
gpu_df = pd.read_csv("GPU_Specs.csv")
laptop_df = pd.read_csv("Laptop_Data.csv")

cpu_df = pd.concat([cpu_df, cpu_new], ignore_index=True)
gpu_df = pd.concat([gpu_df, gpu_new], ignore_index=True)
laptop_df = pd.concat([laptop_df, laptop_new], ignore_index=True)

cpu_df.to_csv("CPU_Specs.csv", index=False)
gpu_df.to_csv("GPU_Specs.csv", index=False)
laptop_df.to_csv("Laptop_Data.csv", index=False)

print("Successfully injected new 2023/2024 modern laptops and parts.")
