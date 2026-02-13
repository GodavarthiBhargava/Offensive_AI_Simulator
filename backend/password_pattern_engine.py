"""
AI Password Pattern Engine - Behavioral Analysis Module
Implements smart password generation based on learned patterns
"""

class PasswordPatternEngine:
    def __init__(self):
        # Character substitution patterns (Leet speak)
        self.char_substitutions = {
            'a': ['@', '4'],
            'e': ['3'],
            'i': ['1', '!'],
            'o': ['0'],
            's': ['$', '5'],
            't': ['7'],
            'l': ['1'],
            'g': ['9'],
            'b': ['8']
        }
        
        # Common number patterns
        self.number_patterns = [
            '123', '1234', '12345', '123456',
            '321', '111', '000', '007',
            '2024', '2025', '2023', '2022', '2021'
        ]
        
        # Special character patterns
        self.special_patterns = [
            '!', '@', '#', '$', '!@#',
            '@123', '!123', '#123',
            '@!', '!@', '@#'
        ]
        
        # Common password bases
        self.common_bases = [
            'password', 'admin', 'welcome', 'qwerty',
            'letmein', 'monkey', 'dragon', 'master',
            'sunshine', 'princess', 'football', 'shadow'
        ]
        
        # Transformation rules (ordered by probability)
        self.transformation_rules = [
            # Rule 1: Base word + numbers
            lambda w: f"{w}123",
            lambda w: f"{w}1234",
            lambda w: f"{w}12345",
            lambda w: f"{w}2024",
            lambda w: f"{w}2025",
            lambda w: f"{w}@123",
            lambda w: f"{w}!123",
            
            # Rule 2: Capitalized + numbers
            lambda w: f"{w.capitalize()}123",
            lambda w: f"{w.capitalize()}1234",
            lambda w: f"{w.capitalize()}@123",
            lambda w: f"{w.capitalize()}2024",
            
            # Rule 3: All caps + numbers
            lambda w: f"{w.upper()}123",
            lambda w: f"{w.upper()}@123",
            
            # Rule 4: Base + special chars
            lambda w: f"{w}!",
            lambda w: f"{w}@",
            lambda w: f"{w}#",
            lambda w: f"{w}@!",
            
            # Rule 5: Capitalized + special
            lambda w: f"{w.capitalize()}!",
            lambda w: f"{w.capitalize()}@",
            lambda w: f"{w.capitalize()}@123",
            
            # Rule 6: Leet speak variations
            lambda w: self.apply_leet_speak(w),
            lambda w: self.apply_leet_speak(w) + "123",
            lambda w: self.apply_leet_speak(w.capitalize()),
            
            # Rule 7: Reverse patterns
            lambda w: f"{w[::-1]}",
            lambda w: f"{w[::-1]}123",
            
            # Rule 8: First letter caps + rest
            lambda w: f"{w[0].upper()}{w[1:]}",
            lambda w: f"{w[0].upper()}{w[1:]}123",
            
            # Rule 9: Double word
            lambda w: f"{w}{w}",
            lambda w: f"{w}{w.capitalize()}",
        ]
    
    def apply_leet_speak(self, word):
        """Apply leet speak transformations"""
        result = word.lower()
        for char, subs in self.char_substitutions.items():
            if char in result:
                result = result.replace(char, subs[0])
        return result
    
    def generate_from_name(self, first_name, last_name, birth_year=None):
        """Generate password candidates from personal information"""
        candidates = []
        
        # Base words
        bases = []
        if first_name:
            bases.extend([first_name.lower(), first_name.capitalize(), first_name.upper()])
        if last_name:
            bases.extend([last_name.lower(), last_name.capitalize(), last_name.upper()])
        if first_name and last_name:
            bases.extend([
                f"{first_name.lower()}{last_name.lower()}",
                f"{first_name[0].lower()}{last_name.lower()}",
                f"{first_name.lower()}{last_name[0].lower()}"
            ])
        
        # Apply transformation rules
        for base in bases:
            for rule in self.transformation_rules:
                try:
                    candidate = rule(base)
                    if candidate and len(candidate) >= 4:
                        candidates.append(candidate)
                except:
                    pass
        
        # Add birth year patterns
        if birth_year:
            year_str = str(birth_year)
            year_short = year_str[-2:]
            
            for base in [first_name.lower() if first_name else '', last_name.lower() if last_name else '']:
                if base:
                    candidates.extend([
                        f"{base}{year_str}",
                        f"{base.capitalize()}{year_str}",
                        f"{base}{year_short}",
                        f"{base.capitalize()}{year_short}",
                        f"{base}@{year_str}",
                        f"{base}@{year_short}",
                    ])
        
        # Remove duplicates while preserving order
        seen = set()
        unique_candidates = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                unique_candidates.append(c)
        
        return unique_candidates[:100]  # Top 100 predictions
    
    def analyze_password_patterns(self, passwords):
        """Analyze patterns in cracked passwords"""
        analysis = {
            'total': len(passwords),
            'length_distribution': Counter(),
            'has_numbers': 0,
            'has_special': 0,
            'has_uppercase': 0,
            'has_lowercase': 0,
            'starts_with_capital': 0,
            'ends_with_numbers': 0,
            'common_suffixes': Counter(),
            'common_prefixes': Counter(),
            'leet_speak_usage': 0,
            'character_frequency': Counter(),
            'pattern_types': Counter()
        }
        
        for pwd in passwords:
            # Length
            analysis['length_distribution'][len(pwd)] += 1
            
            # Character types
            if any(c.isdigit() for c in pwd):
                analysis['has_numbers'] += 1
            if any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in pwd):
                analysis['has_special'] += 1
            if any(c.isupper() for c in pwd):
                analysis['has_uppercase'] += 1
            if any(c.islower() for c in pwd):
                analysis['has_lowercase'] += 1
            
            # Position patterns
            if pwd and pwd[0].isupper():
                analysis['starts_with_capital'] += 1
            
            # Extract numbers at end
            match = re.search(r'\d+$', pwd)
            if match:
                analysis['ends_with_numbers'] += 1
                analysis['common_suffixes'][match.group()] += 1
            
            # Extract prefix (first 3-5 chars if alpha)
            if len(pwd) >= 3:
                prefix = pwd[:3]
                if prefix.isalpha():
                    analysis['common_prefixes'][prefix.lower()] += 1
            
            # Leet speak detection
            if any(c in '@$!0134578' for c in pwd):
                analysis['leet_speak_usage'] += 1
            
            # Character frequency
            for char in pwd:
                analysis['character_frequency'][char] += 1
            
            # Pattern classification
            if pwd.isdigit():
                analysis['pattern_types']['numeric_only'] += 1
            elif pwd.isalpha():
                analysis['pattern_types']['alpha_only'] += 1
            elif pwd.isalnum():
                analysis['pattern_types']['alphanumeric'] += 1
            else:
                analysis['pattern_types']['complex'] += 1
        
        return analysis
    
    def calculate_probabilities(self, analysis):
        """Calculate probability scores for different patterns"""
        total = analysis['total']
        if total == 0:
            return {}
        
        probabilities = {
            'add_numbers': (analysis['has_numbers'] / total) * 100,
            'add_special': (analysis['has_special'] / total) * 100,
            'use_uppercase': (analysis['has_uppercase'] / total) * 100,
            'capitalize_first': (analysis['starts_with_capital'] / total) * 100,
            'numbers_at_end': (analysis['ends_with_numbers'] / total) * 100,
            'use_leet_speak': (analysis['leet_speak_usage'] / total) * 100,
        }
        
        return probabilities
    
    def generate_report(self, analysis, probabilities):
        """Generate detailed behavioral analysis report"""
        total = analysis['total']
        
        report = f"""
╔══════════════════════════════════════════════════════════════════╗
║          AI BEHAVIORAL ANALYSIS - PATTERN LEARNING REPORT        ║
╚══════════════════════════════════════════════════════════════════╝

📊 DATASET OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Passwords Analyzed: {total}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════════════

🧠 LEARNED BEHAVIORAL PATTERNS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. NUMBER USAGE PATTERN
   Probability: {probabilities.get('add_numbers', 0):.1f}%
   Insight: {self._get_insight('numbers', probabilities.get('add_numbers', 0))}
   
2. SPECIAL CHARACTER USAGE
   Probability: {probabilities.get('add_special', 0):.1f}%
   Insight: {self._get_insight('special', probabilities.get('add_special', 0))}
   
3. CAPITALIZATION PATTERN
   First Letter Capital: {probabilities.get('capitalize_first', 0):.1f}%
   Contains Uppercase: {probabilities.get('use_uppercase', 0):.1f}%
   Insight: {self._get_insight('capital', probabilities.get('capitalize_first', 0))}
   
4. NUMBER POSITION PATTERN
   Numbers at End: {probabilities.get('numbers_at_end', 0):.1f}%
   Insight: {self._get_insight('position', probabilities.get('numbers_at_end', 0))}
   
5. LEET SPEAK USAGE
   Probability: {probabilities.get('use_leet_speak', 0):.1f}%
   Insight: {self._get_insight('leet', probabilities.get('use_leet_speak', 0))}

═══════════════════════════════════════════════════════════════════

📏 LENGTH DISTRIBUTION ANALYSIS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self._format_length_distribution(analysis['length_distribution'], total)}

═══════════════════════════════════════════════════════════════════

🎯 PATTERN TYPE DISTRIBUTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self._format_pattern_types(analysis['pattern_types'], total)}

═══════════════════════════════════════════════════════════════════

🔥 MOST COMMON SUFFIXES (Top 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{self._format_top_items(analysis['common_suffixes'], 10)}

═══════════════════════════════════════════════════════════════════

💡 AI PREDICTION STRATEGY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on learned patterns, AI will prioritize:

{self._generate_strategy(probabilities)}

═══════════════════════════════════════════════════════════════════

🎓 TRANSFORMATION RULES RANKING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Priority 1: {self._get_top_rule(probabilities, 1)}
Priority 2: {self._get_top_rule(probabilities, 2)}
Priority 3: {self._get_top_rule(probabilities, 3)}
Priority 4: {self._get_top_rule(probabilities, 4)}
Priority 5: {self._get_top_rule(probabilities, 5)}

═══════════════════════════════════════════════════════════════════

📈 ATTACK EFFICIENCY PREDICTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Using AI-guided approach vs Random:
• Estimated Success Rate: {self._calculate_success_rate(probabilities):.1f}%
• Efficiency Gain: {self._calculate_efficiency(probabilities):.0f}x faster
• Recommended Attack: Smart Pattern-Based

═══════════════════════════════════════════════════════════════════
"""
        return report
    
    def _get_insight(self, pattern_type, probability):
        """Generate insight based on probability"""
        if probability >= 70:
            insights = {
                'numbers': 'Users heavily rely on numbers - prioritize numeric suffixes',
                'special': 'High special character usage - include @!# in predictions',
                'capital': 'Strong capitalization pattern - start with capital letter',
                'position': 'Numbers consistently at end - append 123, 2024, etc.',
                'leet': 'Leet speak common - apply character substitutions'
            }
        elif probability >= 40:
            insights = {
                'numbers': 'Moderate number usage - include in secondary predictions',
                'special': 'Some special character usage - test common symbols',
                'capital': 'Mixed capitalization - try both cases',
                'position': 'Numbers sometimes at end - test suffix patterns',
                'leet': 'Occasional leet speak - include in variations'
            }
        else:
            insights = {
                'numbers': 'Low number usage - deprioritize numeric patterns',
                'special': 'Rare special characters - focus on alphanumeric',
                'capital': 'Lowercase preferred - prioritize lowercase variants',
                'position': 'Numbers not typically at end - try other positions',
                'leet': 'Leet speak rare - standard characters preferred'
            }
        
        return insights.get(pattern_type, 'Pattern detected')
    
    def _format_length_distribution(self, dist, total):
        """Format length distribution"""
        result = ""
        for length in sorted(dist.keys()):
            count = dist[length]
            percentage = (count / total) * 100
            bar = '█' * int(percentage / 2)
            result += f"Length {length:2d}: {bar} {percentage:5.1f}% ({count} passwords)\n"
        return result
    
    def _format_pattern_types(self, types, total):
        """Format pattern types"""
        result = ""
        for ptype, count in types.most_common():
            percentage = (count / total) * 100
            bar = '█' * int(percentage / 2)
            result += f"{ptype:15s}: {bar} {percentage:5.1f}% ({count})\n"
        return result
    
    def _format_top_items(self, counter, limit):
        """Format top items from counter"""
        result = ""
        for item, count in counter.most_common(limit):
            result += f"  • '{item}' - used {count} times\n"
        return result if result else "  No data available\n"
    
    def _generate_strategy(self, probs):
        """Generate attack strategy based on probabilities"""
        strategies = []
        
        if probs.get('capitalize_first', 0) >= 50:
            strategies.append("1. Start with capitalized first letter")
        if probs.get('add_numbers', 0) >= 50:
            strategies.append("2. Append common numbers (123, 2024, etc.)")
        if probs.get('add_special', 0) >= 40:
            strategies.append("3. Add special characters (@, !, #)")
        if probs.get('use_leet_speak', 0) >= 30:
            strategies.append("4. Apply leet speak transformations")
        
        strategies.append("5. Combine personal information with patterns")
        
        return '\n'.join(strategies) if strategies else "Standard dictionary attack"
    
    def _get_top_rule(self, probs, priority):
        """Get top transformation rule by priority"""
        rules = [
            (probs.get('capitalize_first', 0), "Capitalize first letter + numbers"),
            (probs.get('add_numbers', 0), "Base word + numeric suffix"),
            (probs.get('add_special', 0), "Add special characters"),
            (probs.get('use_leet_speak', 0), "Apply leet speak substitution"),
            (probs.get('numbers_at_end', 0), "Append year/common numbers")
        ]
        
        sorted_rules = sorted(rules, key=lambda x: x[0], reverse=True)
        if priority <= len(sorted_rules):
            return f"{sorted_rules[priority-1][1]} ({sorted_rules[priority-1][0]:.1f}% probability)"
        return "Standard transformation"
    
    def _calculate_success_rate(self, probs):
        """Calculate estimated success rate"""
        avg_prob = sum(probs.values()) / len(probs) if probs else 0
        return min(avg_prob * 1.5, 95)
    
    def _calculate_efficiency(self, probs):
        """Calculate efficiency gain"""
        avg_prob = sum(probs.values()) / len(probs) if probs else 0
        return max(avg_prob / 10, 5)
