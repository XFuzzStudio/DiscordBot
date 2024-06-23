import discord
from discord.ext import commands, tasks
import psutil
import socket
import speedtest
import subprocess
import platform
import time
import requests
import GPUtil
from pynvml import nvmlInit, nvmlDeviceGetHandleByIndex, nvmlDeviceGetUtilizationRates, nvmlDeviceGetName

TOKEN = 'BOT TOCKEN'
CHANNEL_ID = CHANNEL_ID  # Replace with your channel ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def get_server_status():
    try:
        # Uptime
        if platform.system() == "Windows":
            uptime = time.time() - psutil.boot_time()
            uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))
        else:
            uptime = subprocess.check_output(['uptime', '-p']).decode('utf-8').strip()
        
        # Disk usage
        disk_usage = psutil.disk_usage('/')
        disk_usage_str = f'Total: {disk_usage.total // (2**30)}GB, Used: {disk_usage.used // (2**30)}GB, Free: {disk_usage.free // (2**30)}GB'
        
        # CPU usage
        cpu_usage = psutil.cpu_percent(interval=1)

        # GPU usage for NVIDIA
        nvmlInit()
        gpus = GPUtil.getGPUs()
        gpu_usage = []
        for gpu in gpus:
            handle = nvmlDeviceGetHandleByIndex(gpu.id)
            utilization = nvmlDeviceGetUtilizationRates(handle)
            gpu_usage.append({
                'name': nvmlDeviceGetName(handle),
                'load': utilization.gpu,
                'memory': utilization.memory
            })

        # RAM usage
        ram = psutil.virtual_memory()
        ram_usage_str = f'Total: {ram.total // (2**30)}GB, Used: {ram.used // (2**30)}GB, Free: {ram.available // (2**30)}GB'
        
        # Network speed
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        speed_results = st.results.dict()
        download_speed = speed_results['download'] / 10**6  # Convert to Mbps
        upload_speed = speed_results['upload'] / 10**6  # Convert to Mbps
        
        # Internal IP address
        hostname = socket.gethostname()
        internal_ip_address = socket.gethostbyname(hostname)
        
        # External IP address
        external_ip_address = requests.get('https://api.ipify.org').text
        
        # Running processes
        processes = [p.info for p in psutil.process_iter(attrs=['pid', 'name'])][:5]  # First 5 processes
        
        return {
            'uptime': uptime_str,
            'disk_usage': disk_usage_str,
            'cpu_usage': f'{cpu_usage}%',
            'gpu_usage': gpu_usage,
            'ram_usage': ram_usage_str,
            'download_speed': f'{download_speed:.2f} Mbps',
            'upload_speed': f'{upload_speed:.2f} Mbps',
            'internal_ip_address': internal_ip_address,
            'external_ip_address': external_ip_address,
            'processes': processes
        }
    except Exception as e:
        return {'error': str(e)}

async def send_status_message(channel):
    status = get_server_status()
    if 'error' in status:
        await channel.send(f'Error retrieving status: {status["error"]}')
    else:
        status_message = (
            f'**Server Status**\n'
            f'🕒 **Uptime:** {status["uptime"]}\n'
            f'💽 **Disk Usage:** {status["disk_usage"]}\n'
            f'⚙️ **CPU Usage:** {status["cpu_usage"]}\n'
            f'🧠 **RAM Usage:** {status["ram_usage"]}\n'
            f'📥 **Download Speed:** {status["download_speed"]}\n'
            f'📤 **Upload Speed:** {status["upload_speed"]}\n'
            f'🏠 **Internal IP Address:** {status["internal_ip_address"]}\n'
            f'🌐 **External IP Address:** {status["external_ip_address"]}\n'
            f'🖥️ **GPU Usage:**\n'
        )
        for gpu in status['gpu_usage']:
            status_message += f' - {gpu["name"]}: Load: {gpu["load"]}% Memory: {gpu["memory"]}%\n'
        status_message += '**Running Processes:**\n'
        for process in status['processes']:
            status_message += f' - PID {process["pid"]}: {process["name"]}\n'
        await channel.send(status_message)

@bot.command()
async def status(ctx):
    await send_status_message(ctx.channel)

@tasks.loop(hours=1)
async def update_status():
    channel = bot.get_channel(CHANNEL_ID)
    await send_status_message(channel)

@bot.event
async def on_ready():
    update_status.start()

bot.run(TOKEN)