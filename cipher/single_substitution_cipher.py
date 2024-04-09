def frequency_analysis(text):
    
    # 暗号文内の各文字の出現回数をカウント
    letter_frequency = {} #dictionary
    for letter in ciphertext:
        if letter.isalpha():
            letter = letter.lower()
            if letter in letter_frequency:
                letter_frequency[letter] += 1
            else:
                letter_frequency[letter] = 1
    
    # 頻度でソートされた文字リストを作成。降順に指定。
    sorted_letters = sorted(letter_frequency, key=letter_frequency.get, reverse=True)
    return sorted_letters, letter_frequency


def  decrypt_with_frequency_analysis(ciphertext):
    common_letters = 'etaoinshrdlcumwfgypbvkjxqz'
    sorted_letters, letter_frequency = frequency_analysis(ciphertext)
    
    # 暗号文を解読
    decrypted = ""
    for letter in ciphertext:
        if letter.lower() in letter_frequency:
            index = sorted_letters.index(letter.lower())
            if index < len(common_letters):
                replace_letter = common_letters[index]
                decrypted += replace_letter.upper() if letter.isupper() else replace_letter
            else:
                decrypted += letter
        else:
            decrypted += letter

    return decrypted
    
ciphertext = '''Cempri aoa ctrabqofnwlqr oxpefric rlej dcei ioi airocotbdrw
 dme oiCy aoa pun ed ei do aiawai oicccqic usdeo qdbiroqCy eoipYcti.
   Xy rwwleqo db dri owct faooi r iddic aoa faopebdeo diro do dri oxwidaiq
     qdbiroqieci eo Ooprecd, ioi fao ctmb do oebdi diro up aoa qbeyoiurBb
       biyrbir dri ifetoepr oiCCiqi. Dcei wfaioci oib dbri cioi dooi,
         xud weid yfbidcii, ed xiawic qctdib aoa owfi eoadedp.
           Kiid yfbidcdeq aoa oaiiC dri yfwaiCC iq aiawdeoep.'''
decrypted_message = decrypt_with_frequency_analysis(ciphertext)
print(f"Decrypted message: {decrypted_message}")