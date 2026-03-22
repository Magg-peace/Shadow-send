import streamlit as st
import base64, hashlib
from PIL import Image
import numpy as np
from cryptography.fernet import Fernet, InvalidToken
from io import BytesIO

DELIM = b"<<END>>"

# ---------- SECURITY ----------
def key(p):
    return base64.urlsafe_b64encode(hashlib.sha256(p.encode()).digest())

def encrypt(msg,p):
    return Fernet(key(p)).encrypt(msg.encode())

def decrypt(token,p):
    return Fernet(key(p)).decrypt(token).decode()

# ---------- STEGANOGRAPHY ----------
def encode_fast(img_array, payload):
    bits = np.unpackbits(np.frombuffer(payload+DELIM, dtype=np.uint8))
    flat = img_array.flatten()
    flat[:len(bits)] = (flat[:len(bits)] & 0xFE) | bits
    return flat.reshape(img_array.shape)

def decode_fast(img_array):
    flat = img_array.flatten()
    bits = flat & 1

    byte_list = []
    for i in range(0, len(bits), 8):
        byte = 0
        for b in bits[i:i+8]:
            byte = (byte << 1) | b
        
        byte_list.append(byte)

        if bytes(byte_list[-len(DELIM):]) == DELIM:
            return bytes(byte_list[:-len(DELIM)])

    raise ValueError("No hidden data")

# ---------- PASSWORD STRENGTH ----------
def strength(p):
    score = sum([
        len(p)>=8,
        any(c.isupper() for c in p),
        any(c.isdigit() for c in p),
        any(c in "!@#$%^&*" for c in p)
    ])
    return ["Weak ❌","Medium ⚠️","Strong 🔥"][min(score,2)]

# ---------- UI ----------
st.set_page_config(page_title="ShadowSend PRO", layout="centered")

st.markdown("""
<style>
body { background-color:#0f172a; }
.block-container { padding: 2rem; }
.stButton>button {
    background: linear-gradient(90deg,#38bdf8,#6366f1);
    color:white;
    border-radius:8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🔐 ShadowSend PRO")
st.caption("Secure Image Messaging using Cryptography + Steganography")

tab1, tab2 = st.tabs(["📤 Encode", "📥 Decode"])

# ---------- ENCODE ----------
with tab1:
    img_file = st.file_uploader("Upload Image", type=["png","jpg"], key="encode_img")
    msg = st.text_area("Secret Message", key="encode_msg")
    pwd = st.text_input("Password", type="password", key="encode_pwd")

    if pwd:
        st.info(f"Password Strength: {strength(pwd)}")

    if st.button("🚀 Encode", key="encode_btn"):
        if img_file and msg and pwd:
            img = Image.open(img_file).convert("RGB").resize((512,512))
            arr = np.array(img)

            token = encrypt(msg,pwd)
            stego = encode_fast(arr,token)

            out_img = Image.fromarray(stego.astype(np.uint8))

            st.image([img,out_img], caption=["Original","Encoded"])

            buf = BytesIO()
            out_img.save(buf, format="PNG")

            st.success("✅ Message Hidden Successfully!")
            st.download_button("📥 Download Image", buf.getvalue(), "secret.png")

# ---------- DECODE ----------
with tab2:
    img_file = st.file_uploader("Upload Secret Image", type=["png","jpg"], key="decode_img")
    pwd = st.text_input("Password", type="password", key="decode_pwd")

    if st.button("🔍 Decode", key="decode_btn"):
        if img_file and pwd:
            img = Image.open(img_file).convert("RGB").resize((512,512))
            arr = np.array(img)

            try:
                token = decode_fast(arr)
                msg = decrypt(token,pwd)
                st.success("🔓 Message Revealed:")
                st.write(msg)
            except InvalidToken:
                st.error("❌ Wrong Password")
            except:
                st.error("❌ No hidden data found")
