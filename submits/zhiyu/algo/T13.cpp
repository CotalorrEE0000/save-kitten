class Solution {
   public:
    int romanToInt(string s) {
        const char* l = "IVXLCDM";
        int a[] = {1, 5, 10, 50, 100, 500, 1000};
        int len = s.size();
        int sum = 0;
        int last = 1000;
        for (int i = 0; i < len; i++) {
            int add = 0;
            for (int j = 0; j < 7; j++) {
                if (s[i] == l[j]) {
                    add = a[j];
                    break;
                }
            }
            sum = sum + add;
            if (add > last) {
                sum = sum - last * 2;
            }
            last = add;
        }
        return sum;
    }
};
